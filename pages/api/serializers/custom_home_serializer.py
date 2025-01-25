from rest_framework.serializers import Serializer
from rest_framework.serializers import IntegerField
from projects.api.serializers import ContentSerializer
from testimonial.api.serializers import TestimonialSerializer


class CustomHomeSerializer(Serializer):
    featured_projects = ContentSerializer(many=True)
    featured_blogs = ContentSerializer(many=True)
    testimonials = TestimonialSerializer(many=True)
    ticket = IntegerField()
