from rest_framework.generics import ListCreateAPIView
from contents.models import ContentTypeModel
from contents.api.serializers import ContentTypeSerializer


class ContentsView(ListCreateAPIView):
    queryset = ContentTypeModel.objects.all()
    serializer_class = ContentTypeSerializer
    authentication_classes = []
