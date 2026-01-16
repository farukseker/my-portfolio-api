from django.contrib import admin
from .models import OTPModel
from unfold.admin import ModelAdmin


admin.site.register(OTPModel, ModelAdmin)

