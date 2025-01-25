from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import ContentModel
from testimonial.models import Testimonial
from pages.api.serializers import CustomHomeSerializer
from pages.models import PageModel
from analytical.utils import ViewCountWithRule


class CustomHomeView(APIView):
    serializer_class = CustomHomeSerializer

    def get_queryset(self):
        page: PageModel = PageModel.objects.filter(pk='home').first()
        view = ViewCountWithRule(page, self.request)
        view = view()
        return {
            "featured_projects": ContentModel.objects.filter(show=True, content_type__name='project', is_featured=True),
            "featured_blogs": ContentModel.objects.filter(show=True, content_type__name='blog', is_featured=True),
            "testimonials": Testimonial.objects.filter(approved=True),
            "ticket": view.id
        }

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_queryset()).data)
