from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from custom_auth.models import OTPModel


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        has_otp = OTPModel.user_has_otp_device(self.user)
        return {
            "username": self.user.username,
            "email": self.user.email,
            "has_otp": has_otp,
            # "permissions": self.user.user_permissions.values_list("codename", flat=True),
            # "groups": self.user.groups.values_list("name", flat=True),
            **attrs,
        }

