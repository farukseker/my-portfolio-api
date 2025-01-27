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
            "featured_projects": self.content_loader(show=True, content_type__name='project', is_featured=True),
            "featured_blogs": self.content_loader(show=True, content_type__name='blog', is_featured=True),
            "testimonials": self.get_testimonials(),
            "ticket": view.id
        }

    @staticmethod
    def content_loader(**kwargs):
        return ContentModel.objects.filter(**kwargs)

    @staticmethod
    def get_testimonials():
        return Testimonial.objects.filter(approved=True)

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_queryset()).data)
