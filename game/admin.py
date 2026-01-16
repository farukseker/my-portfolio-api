from django.contrib import admin
from game import models
from unfold.admin import ModelAdmin


admin.site.register(models.GameInfoModel, ModelAdmin)
admin.site.register(models.MusicInfoModel, ModelAdmin)
admin.site.register(models.GameVideoModel, ModelAdmin)



