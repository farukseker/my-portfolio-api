from django.contrib import admin
from unfold.admin import ModelAdmin

from chatwithme.models import ChatRoom, ChatLog, MeetingModel

admin.site.register(ChatRoom, ModelAdmin)
admin.site.register(ChatLog, ModelAdmin)
admin.site.register(MeetingModel, ModelAdmin)