from django.urls import path, include
from . import views


app_name = "pages"


urlpatterns = [
    # path('analytics/<str:name>/', PageView.as_view(), name='page-analytics'),
    path('custom-home/', views.CustomHomeView.as_view(), name="custom_home"),
    path('navbar/<str:name>/', views.NavbarView.as_view(), name='navbar'),
    path('<str:name>/', views.PageView.as_view(), name='page'),
]


