from pages.models import PageModel
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from pages.api.serializers import PagesAnalyticsSerializer


class PagesAnalyticsView(RetrieveAPIView):
    serializer_class = PagesAnalyticsSerializer
    queryset = PageModel.objects.all()
    lookup_field = 'name'
    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

