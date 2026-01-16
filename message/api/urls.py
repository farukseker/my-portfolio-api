from django.contrib import admin
from django.urls import path
from django.conf import settings

from .views import CreateMessageView

app_name = "message"

urlpatterns = [
    path('create/', CreateMessageView.as_view(), name='create_message'),

]


