from django.db import models
from datetime import datetime

from projects.models import TurkishAutoSlugField


class CertificateModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def is_out_able(self):
        return self.end_date is None or self.end_date > datetime.now().date()


class CertificateProviderModel(models.Model):
    name = models.CharField(max_length=255)
    slug = TurkishAutoSlugField(
        populate_from='name',
        unique=True,
        editable=True,
        blank=True,
        always_update=True,
    )
    logo = models.URLField()
    url = models.URLField()
    description = models.TextField()
    certificates = models.ManyToManyField(CertificateModel)
