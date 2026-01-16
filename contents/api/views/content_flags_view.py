from rest_framework.generics import RetrieveAPIView
from contents.models import ContentTypeModel
from contents.api.serializers import ContentTypeSerializer


class ContentFlagsView(RetrieveAPIView):
    authentication_classes = []
    lookup_field = 'name'
    queryset = ContentTypeModel
    serializer_class = ContentTypeSerializer
