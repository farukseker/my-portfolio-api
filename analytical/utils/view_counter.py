import logging
from django.apps import apps
from django.utils import timezone
from django.conf import settings
from django.tasks import task  # Kullandığınız kütüphane

from ..models import IPRefModel, IPRequestMeta, ViewModel
from .ip_data import get_ip_data

logger = logging.getLogger('ViewTask')


@task
def process_view_task(app_label, model_name, object_id, ip_address, meta_data, hourly_cooldown=True):
    """
    Bu fonksiyon arka planda çalışır. Request objesine erişimi yoktur.
    Tüm veriyi parametre olarak alır.
    """
    try:
        # 1. Page objesini dinamik olarak tekrar çekiyoruz
        model_class = apps.get_model(app_label, model_name)
        page = model_class.objects.get(pk=object_id)
        if page:
            print('page war moruk ', page)
    except model_class.DoesNotExist:
        logger.error(f"Page object not found | {app_label}.{model_name} id={object_id}")
        return

    logger.debug(f"Task started | page={object_id} ip={ip_address}")

    # --- Yardımcı Fonksiyonlar (Task İçinde) ---
    def get_last_visit_view():
        if ip_ref := IPRefModel.objects.filter(ip_address=ip_address).first():
            return page.view.filter(ip=ip_ref).order_by('-visit_time').first()
        return None

    def can_proceed():
        if IPRefModel.objects.filter(ip_address=ip_address, is_blocked=True).exists():
            logger.info(f"Blocked IP | {ip_address}")
            return False

        if hourly_cooldown:
            if vs := get_last_visit_view():
                now = timezone.now()
                if vs.visit_time.day == now.day:
                    return not (vs.visit_time.hour == now.hour)
        return True

    if can_proceed():
        logger.debug(f"Creating new view | ip={ip_address}")

        ip_defaults = {}
        if not settings.DEBUG:
            try:
                ip_defaults = get_ip_data(ip_address)
            except Exception as e:
                logger.error(f"IP Data Error: {e}")

        ip_obj, created = IPRefModel.objects.update_or_create(
            ip_address=ip_address,
            defaults=ip_defaults
        )

        fingerprint = IPRequestMeta.build_fingerprint(
            user_agent=str(meta_data.get('user_agent')),
            http_sec_ch_ua=meta_data.get('http_sec_ch_ua'),
            request_type=meta_data.get('request_method'),
        )

        IPRequestMeta.objects.get_or_create(
            ip=ip_obj,
            fingerprint=fingerprint,
            defaults={
                "user_agent": str(meta_data.get('user_agent')),
                "http_sec_ch_ua": meta_data.get('http_sec_ch_ua'),
                "query_string": meta_data.get('query_string'),
                "request_type": meta_data.get('request_method'),
                "request_data": meta_data.get('request_data')[:500],
            },
        )

        view = ViewModel.objects.create(
            visit_time=timezone.now(),
            ip=ip_obj,
        )

        page.view.add(view)

    else:
        logger.debug(f"Reusing last view | ip={ip_address}")
        if view := get_last_visit_view():
            view.reload_count_in_a_clock += 1
            view.save()


import logging


class ViewCountWithRule:
    def __init__(self, page: object | None, request, hourly_cooldown: bool = True):
        self.logger = logging.getLogger('ViewCountWithRule')
        self.page = page
        self.request = request
        self.hourly_cooldown = hourly_cooldown

        self.ip_address = self.get_client_ip()
        self.meta_data = self.extract_meta_data()

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else self.request.META.get('REMOTE_ADDR')
        return ip

    def extract_meta_data(self):
        data = getattr(self.request, 'data', None)
        if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
            data = str(data)

        return {
            "user_agent": self.request.META.get('HTTP_USER_AGENT', ''),
            "http_sec_ch_ua": self.request.META.get("HTTP_SEC_CH_UA"),
            "query_string": self.request.META.get("QUERY_STRING"),
            "request_method": self.request.META.get("REQUEST_METHOD"),
            "request_data": data,
        }

    def __call__(self):
        if not self.page:
            return

        self.logger.debug(f"Dispatching task for page {self.page.__dict__}")

        process_view_task.enqueue(
            app_label=self.page._meta.app_label,
            model_name=self.page._meta.model_name,
            object_id=self.page.pk if self.page else None,
            ip_address=self.ip_address,
            meta_data=self.meta_data,
            hourly_cooldown=self.hourly_cooldown
        )