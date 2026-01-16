from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin


admin.site.register(models.ContentModel, ModelAdmin)
admin.site.register(models.ContentTypeModel, ModelAdmin)
admin.site.register(models.ContentCommentModel, ModelAdmin)

