from django.db import models


class IPRefModel(models.Model):
    ip_address = models.CharField(max_length=120, unique=True)
    is_blocked = models.BooleanField(default=False)

    country=models.CharField(max_length=50)
    country_code=models.CharField(max_length=50)
    region=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    lat=models.CharField(max_length=50)
    lon=models.CharField(max_length=50)
    isp=models.CharField(max_length=50)
    org=models.CharField(max_length=50)
    asn=models.CharField(max_length=50)

    user_agent = models.TextField(null=True, default=None, blank=True, editable=False)
    query_string = models.TextField(null=True, default=None, blank=True)
    request_type = models.CharField(max_length=20, null=True, default=None, blank=True)
    http_sec_ch_ua = models.TextField(null=True, default=None, blank=True)
    request_data = models.TextField(null=True, default=None, blank=True)

