from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import pyotp


"""
FEATURE ; OTP SERVICE
-------------------------------

[ ] REGISTER DEVICE WITH MAIL

"""


class OTPModelManager(models.Manager):
    def user_has_otp_device(self, user):
        try:
            otp_instance = self.get(user=user)
            return True
        except self.model.DoesNotExist:
            return False


class OTPModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    otp_device = models.TextField(max_length=255, editable=True)
    is_active = models.BooleanField(default=True)


    def create_hash(self):

        return pyotp.TOTP(self.otp_device).provision
        ing_uri(name=self.user.email, issuer_name=self.user.username)

    def qr_code(self):
        import pyotp
        pyotp.TOTP.generate_otp()

    def load_otp(self):
        pass

    def otp_verify(self, code: str):
        totp = pyotp.TOTP(self.otp_device)
        return totp.verify(code)

    # object = OTPModelManager()

    @classmethod
    def user_has_otp_device(cls, user):
        return cls.objects.filter(user=user).exists()

