from rest_framework.generics import ListCreateAPIView
from testimonial.api.serializers import TestimonialSerializer
from testimonial.models import Testimonial


class TestimonialListCreateView(ListCreateAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    authentication_classes = []
