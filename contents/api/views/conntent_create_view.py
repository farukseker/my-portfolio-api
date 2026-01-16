from rest_framework.generics import CreateAPIView

from contents.api.serializers import ContentSerializer


class ContentCreateView(CreateAPIView):
    serializer_class = ContentSerializer

