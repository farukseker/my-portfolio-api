from rest_framework.generics import ListAPIView
from testimonial.api.serializers import TestimonialSerializer
from testimonial.models import Testimonial


class TestimonialListView(ListAPIView):
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
