from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin


admin.site.register(models.PageModel, ModelAdmin)
# admin.site.register(models.ContextModel)
admin.site.register(models.ContextFieldModel, ModelAdmin)
admin.site.register(models.NavbarModel, ModelAdmin)
admin.site.register(models.NavbarItemModel, ModelAdmin)