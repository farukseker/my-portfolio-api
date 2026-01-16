from django.urls import path
from game.api import views

app_name: str = "game"

urlpatterns = [
    path('', views.GameListView.as_view(), name='games'),
    path('<slug>', views.GameVideoView.as_view(), name='game')
]