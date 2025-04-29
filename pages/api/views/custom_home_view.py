from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import ContentModel
from testimonial.models import Testimonial
from pages.api.serializers import CustomHomeSerializer
from pages.models import PageModel
from analytical.utils import ViewCountWithRule
from performance import get_performance_metric


class CustomHomeView(APIView):
    serializer_class = CustomHomeSerializer

    @get_performance_metric
    def get_queryset(self):
        page: PageModel = PageModel.objects.filter(pk='home').first()
        view = ViewCountWithRule(page, self.request)
        view = view()
        return {
            "ticket": view.id
        }

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_queryset()).data)
