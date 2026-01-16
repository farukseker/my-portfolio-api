
from rest_framework.generics import ListAPIView
from contents.api.serializers import ContentListSerializer
from contents.models import ContentModel
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from django.db.models import Q


class AdminAllProjectsListView(ListAPIView):
    serializer_class = ContentListSerializer
    filter_backends: list = [SearchFilter, OrderingFilter]
    search_fields: tuple = 'title', 'content_type__name', 'tags__id'
    queryset = ContentModel.objects.order_by('-update')
    lookup_field = 'content_type'

