from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *


admin.site.register(TagModel, ModelAdmin)
admin.site.register(TagCategoryModel, ModelAdmin)
