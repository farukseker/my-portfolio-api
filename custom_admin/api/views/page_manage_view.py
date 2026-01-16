from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from pages.api.serializers import PageAdminSerializer
from pages.models import PageModel


class PageManageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PageAdminSerializer
    lookup_field = 'name'
    queryset = PageModel

    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]
