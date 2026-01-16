from rest_framework.generics import ListAPIView
from analytical.utils import ViewCountWithRule
from game.api.serializers import GameVideoListSerializer
from game.models import GameVideoModel


class GameListView(ListAPIView):
    authentication_classes = []
    serializer_class = GameVideoListSerializer
    queryset = GameVideoModel.objects.filter(show=True)

    # def get_object(self):
    #     obj = super().get_object()
    #     ViewCountWithRule(obj, self.request)()
    #     return obj
