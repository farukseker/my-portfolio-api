from django.db import models


class IPRefModel(models.Model):
    ip_address = models.CharField(max_length=120, unique=True)
    is_blocked = models.BooleanField(default=False)

    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    isp = models.CharField(max_length=50)
    org = models.CharField(max_length=50)
    asn = models.CharField(max_length=50)

import hashlib


class IPRequestMeta(models.Model):
    ip = models.ForeignKey(
        IPRefModel,
        on_delete=models.CASCADE,
        related_name="requests",
    )

    user_agent = models.TextField(null=True, blank=True)
    http_sec_ch_ua = models.TextField(null=True, blank=True)
    query_string = models.TextField(null=True, blank=True)
    request_type = models.CharField(max_length=20, null=True, blank=True)
    request_data = models.TextField(null=True, blank=True)

    fingerprint = models.CharField(
        max_length=64,
        editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ip", "fingerprint"],
                name="uniq_ip_meta_fingerprint"
            )
        ]

    @staticmethod
    def build_fingerprint(user_agent, http_sec_ch_ua, request_type):
        raw = f"{user_agent or ''}|{http_sec_ch_ua or ''}|{request_type or ''}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        raw = f"{self.user_agent}|{self.http_sec_ch_ua}|{self.request_type}"
        self.fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)
