from django.contrib import admin
from testimonial.models import Testimonial
from unfold.admin import ModelAdmin


admin.site.register(Testimonial, ModelAdmin)
