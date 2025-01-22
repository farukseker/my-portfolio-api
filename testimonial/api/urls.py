from django.urls import path, include
from testimonial.api.views import TestimonialListCreateView

app_name = "testimonial"

urlpatterns = [
    path('', TestimonialListCreateView.as_view(), name='testimonial_list_create'),
]
