from django.urls import path, include
from testimonial.api.views import TestimonialListView

app_name = "testimonial"

urlpatterns = [
    path('', TestimonialListView.as_view(), name='testimonial_list_create'),
]
