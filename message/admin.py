from django.contrib import admin
from .models import MessageModel
from unfold.admin import ModelAdmin

admin.site.register(MessageModel, ModelAdmin)

