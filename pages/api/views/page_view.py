from rest_framework.generics import RetrieveAPIView
from pages.models import PageModel
from pages.api.serializers import PageSerializer
from analytical.utils import ViewCountWithRule


class PageView(RetrieveAPIView):
    lookup_field = 'name'
    queryset = PageModel
    serializer_class = PageSerializer
    authentication_classes = []
    permission_classes = []

    def get_object(self):
        obj = super().get_object()
        ViewCountWithRule(obj, self.request)()
        return obj
