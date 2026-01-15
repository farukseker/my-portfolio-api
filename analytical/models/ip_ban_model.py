from django.db import models


class IPBanModel(models.Model):
    ip_address = models.CharField(max_length=120, unique=True)

