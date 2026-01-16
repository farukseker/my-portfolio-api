from django.conf import settings
from rest_framework.generics import RetrieveAPIView

from analytical.utils import ViewCountWithRule
from game.api.serializers import GameVideoSerializer
from game.models import GameVideoModel


class GameVideoView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = GameVideoSerializer
    lookup_field = 'slug'
    queryset = GameVideoModel

    def get_object(self):
        obj = super().get_object()
        ViewCountWithRule(obj, self.request, not settings.DEBUG)()
        return obj

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return GameVideoModel.objects.all()
        return GameVideoModel.objects.filter(show=True)



