from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.db.models import Count, F
from django.db.models.functions import ExtractYear

class MatrixAnalyticView(RetrieveAPIView):  # lydia
    lookup_field = 'name'
    # serializer_class =

    def get_queryset(self):
        print(self.kwargs)
        return []


'''
from pages.models import PageModel
from rest_framework.generics import RetrieveAPIView

from pages.api.serializers import PagesAnalyticsSerializer


class PagesAnalyticsView(RetrieveAPIView):
    serializer_class = PagesAnalyticsSerializer
    queryset = PageModel.objects.all()
    lookup_field = 'name'
'''