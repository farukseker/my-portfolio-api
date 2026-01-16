from rest_framework.generics import RetrieveAPIView
from pages.api.serializers import NavbarSerializer
from pages.models import NavbarModel


class NavbarView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = NavbarSerializer
    queryset = NavbarModel
    lookup_field = 'name'

