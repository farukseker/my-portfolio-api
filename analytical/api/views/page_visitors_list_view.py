from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from analytical.api.serializers import ViewSerializer
from pages.models import PageModel
from django.shortcuts import get_object_or_404


class VisitorsResultsPageNumberPagination(PageNumberPagination):
    max_page_size: int = 100
    page_size: int = 20
    page_size_query_param: str = 'results_size'


class PageVisitorsListView(ListAPIView):
    lookup_field: str = 'name'
    filter_backends: list = SearchFilter, OrderingFilter
    search_fields: list = 'user_agent', 'ip_address', 'ip_data', 'visit_time'
    ordering_fields: list = 'visit_time', 'reload_count_in_a_clock'
    serializer_class = ViewSerializer
    pagination_class = VisitorsResultsPageNumberPagination
    permission_classes = [
        IsAuthenticated,
        IsAdminUser
    ]

    def get(self, request, *args, **kwargs):
        page_model: PageModel = get_object_or_404(PageModel, **{self.lookup_field: kwargs.get(self.lookup_field)})
        views = page_model.get_view()
        self.queryset = views.order_by('-visit_time')
        return super().get(request, *args, **kwargs)
