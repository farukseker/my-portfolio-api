from django.contrib import admin
from unfold.admin import ModelAdmin


from .models import CloudinaryTest

admin.site.register(CloudinaryTest, ModelAdmin)