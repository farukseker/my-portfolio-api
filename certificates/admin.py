from django.contrib import admin
from unfold.admin import ModelAdmin
from certificates import models


admin.site.register(models.CertificateProviderModel, ModelAdmin)
admin.site.register(models.CertificateModel, ModelAdmin)



