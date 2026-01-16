from rest_framework.permissions import BasePermission
from custom_auth.models import OTPModel


class OtpAllow(BasePermission):
    def has_permission(self, request, view) -> bool:
        if OTPModel.user_has_otp_device(request.user):
            return request.session.get('session_authorization')
        return True

