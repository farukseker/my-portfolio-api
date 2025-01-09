from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from projects.models import ContentModel
from pages.api.serializers import CustomHomeSerializer


class CustomHomeView(GenericAPIView):
    serializer_class = CustomHomeSerializer

    def get_queryset(self):
        return {
            "featured_projects": ContentModel.objects.filter(show=True, content_type__name='project', is_featured=True),
            "featured_blogs": ContentModel.objects.filter(show=True, content_type__name='blog', is_featured=True)
        }
