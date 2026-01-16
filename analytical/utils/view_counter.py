from ..models import ViewModel, IPRefModel, IPRequestMeta
from django.utils import timezone
import logging
from .ip_data import get_ip_data
from django.conf import settings
# from config.settings.base import CUSTOM_LOGGER


class ViewCountWithRule:
    def __init__(self, page, request, hourly_cooldown: bool = True):
        self.logger = logging.getLogger('ViewCountWithRule')
        self.page = page
        self.request = request
        self.ip_address = self.get_client_ip()
        self.use_hourly_cooldown = hourly_cooldown

        self.logger.debug(
            "Initialized | page=%s ip=%s hourly_cooldown=%s",
            getattr(page, "id", None),
            self.ip_address,
            hourly_cooldown,
        )

    def can(self):
        if self.page is None:
            self.logger.error("Page object is None")
            raise ModuleNotFoundError('An object that can be counted is not defined')

        if IPRefModel.objects.filter(ip_address=self.ip_address, is_blocked=True).exists():
            self.logger.info("Blocked IP detected | ip=%s", self.ip_address)
            return False

        if self.use_hourly_cooldown:
            if vs := self.get_last_visit_view():
                now = timezone.now()
                self.logger.debug(
                    "Last visit found | ip=%s last_visit=%s now=%s",
                    self.ip_address,
                    vs.visit_time,
                    now,
                )
                if vs.visit_time.day == now.day:
                    return not vs.visit_time.hour == now.hour

        self.logger.debug("View allowed | ip=%s", self.ip_address)
        return True

    def get_last_visit_view(self):
        if ip_ref := IPRefModel.objects.filter(ip_address=self.ip_address).first():
            view = self.page.view.filter(ip=ip_ref).order_by('-visit_time').first()
            self.logger.debug(
                "Fetched last view | ip=%s view_id=%s",
                self.ip_address,
                getattr(view, "id", None),
            )
            return view

        self.logger.debug("No IPRefModel found | ip=%s", self.ip_address)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else self.request.META.get('REMOTE_ADDR')
        self.logger.debug("Resolved client IP | ip=%s", ip)
        return ip

    def is_admin_user(self):
        is_admin = self.request.user.is_authenticated and self.request.user.is_superuser
        self.logger.debug("Admin check | ip=%s is_admin=%s", self.ip_address, is_admin)
        return is_admin

    def get_user_agent(self):
        if meta := self.request.META.get('HTTP_USER_AGENT', None):
            return meta
        elif hasattr(self.request, 'META'):
            self.logger.error("HTTP_USER_AGENT missing | META=%s", self.request.META)
        else:
            self.logger.error("Request has no META attribute")
        return None

    def get_ip_data(self):
        if settings.DEBUG:
            self.logger.debug("Skipping IP data lookup (DEBUG=True)")
            return {}
        try:
            return get_ip_data(self.ip_address)
        except Exception as ERR:
            self.logger.exception(
                "IP data lookup failed | ip=%s error=%s",
                self.ip_address,
                ERR,
            )
            ...

    def action(self):
        if self.can():
            self.logger.debug("Creating new view | ip=%s", self.ip_address)
            view = self.create_view()
            self.page.view.add(view)
        else:
            self.logger.debug("Reusing last view | ip=%s", self.ip_address)
            view = self.get_last_visit_view()
            view.reload_count_in_a_clock += 1

        view.save()
        self.logger.debug(
            "View saved | view_id=%s reload_count=%s",
            view.id,
            getattr(view, "reload_count_in_a_clock", None),
        )
        return view

    def get_cleaned_data(self) -> dict | None:
        data = self.request.data if hasattr(self.request, 'data') else None
        self.logger.debug("Request data extracted | has_data=%s", bool(data))
        return data

    def create_view(self):
        print(self.__dict__)
        ip, created = IPRefModel.objects.update_or_create(
            ip_address=self.ip_address,
            defaults=get_ip_data(self.ip_address),
        )

        fingerprint = IPRequestMeta.build_fingerprint(
            user_agent=str(self.get_user_agent()),
            http_sec_ch_ua=self.request.META.get("HTTP_SEC_CH_UA"),
            request_type=self.request.META.get("REQUEST_METHOD"),
        )

        IPRequestMeta.objects.get_or_create(
            ip=ip,
            fingerprint=fingerprint,
            defaults={
                "user_agent": str(self.get_user_agent()),
                "http_sec_ch_ua": self.request.META.get("HTTP_SEC_CH_UA"),
                "query_string": self.request.META.get("QUERY_STRING"),
                "request_type": self.request.META.get("REQUEST_METHOD"),
                "request_data": self.get_cleaned_data(),
            },
        )


        if created:
            self.logger.warning(
                "IPRefModel not found, created new | ip=%s",
                self.ip_address,
            )
        else:
            self.logger.debug(
                "IPRefModel exists | ip=%s",
                self.ip_address,
            )

        view = ViewModel.objects.create(
            visit_time=timezone.now(),
            ip=ip,
        )

        self.logger.debug(
            "ViewModel created | view_id=%s ip=%s",
            view.id,
            self.ip_address,
        )
        return view

    def __call__(self, *args, **kwargs):
        self.logger.debug("ViewCountWithRule called")
        return self.action()
