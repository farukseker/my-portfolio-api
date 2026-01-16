from django.urls import path, include
from . import views

app_name = "custom_admin"

urlpatterns = [
    path('page/', views.PageListView.as_view(), name='page-manage'),
    path('page/<str:name>/', views.PageManageRetrieveUpdateDestroyAPIView.as_view(), name='page-manage'),
    path('page/<str:name>/analytics/', views.PagesAnalyticsView.as_view(), name='page-analytic'),
]


