from rest_framework import serializers
from testimonial.models import Testimonial


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        # fields: str = '__all__'
        exclude: tuple = 'approved',  # if bad user set with approved=True had already set approved
