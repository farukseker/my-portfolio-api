from ..models import ViewModel
from django.utils import timezone
import logging
from .ip_data import get_ip_data
from django.conf import settings
# from config.settings.base import CUSTOM_LOGGER


class ViewCountWithRule:
    def __init__(self, page, request, hourly_cooldown: bool = True):
        self.page = page
        self.request = request
        self.ip_address = self.get_client_ip()
        self.use_hourly_cooldown = hourly_cooldown
        self.logger = logging.getLogger('ViewCountWithRule')

    def can(self):
        if self.page is None:
            raise ModuleNotFoundError('An object that can be counted is not defined')
        if self.use_hourly_cooldown:
            if vs := self.get_last_visit_view():
                now = timezone.now()
                if vs.visit_time.day == now.day:
                    return not vs.visit_time.hour == now.hour
        return True

    def get_last_visit_view(self):
        return self.page.view.all().filter(ip_address=self.ip_address).order_by('-visit_time').first()

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else self.request.META.get('REMOTE_ADDR')

    def is_admin_user(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def get_user_agent(self):
        try:
            return self.request.META['HTTP_USER_AGENT']
        except Exception as error:
            self.logger.error(error)
            if hasattr(self.request, 'META'):
                self.logger.error(self.request.META)
            else:
                self.logger.error('request is not have META')
            return

    def get_ip_data(self):
        if settings.DEBUG:
            return {}
        try:
            return get_ip_data(self.ip_address)
        except Exception as ERR:
            ...
            # CUSTOM_LOGGER.construct(
            #     title='ip query service',
            #     error=ERR,
            #     metadata=f'{self.ip_address}'
            # )
            # CUSTOM_LOGGER.send()

    def action(self):
        if self.can():
            view = self.create_view()
            self.page.view.add(view)
        else:
            view = self.get_last_visit_view()
            view.reload_count_in_a_clock += 1
        view.save()
        return view

    def get_cleaned_data(self) -> dict | None:
        return self.request.data if hasattr(self.request, 'data') else None

    def create_view(self):
        return ViewModel.objects.create(
                visit_time=timezone.now(),
                ip_address=self.ip_address,
                is_i_am=self.is_admin_user(),
                ip_data=self.get_ip_data(),
                user_agent=str(self.get_user_agent()),
                query_string=self.request.META.get('QUERY_STRING', None),
                request_type=self.request.META.get('REQUEST_METHOD', None),
                http_sec_ch_ua=self.request.META.get('HTTP_SEC_CH_UA', None),
                request_data=self.get_cleaned_data()
            )

    def __call__(self, *args, **kwargs):
        return self.action()

