from django.urls import path
from chatwithme.api.views import MeetingCreateView, MeetingRetrieveUpdateDestroyView
import uuid

app_name = "chat"

urlpatterns = [
    path('organize-meeting', MeetingCreateView.as_view(), name='create-meeting'),
    path('organize-meeting/<uuid:meeting_id>', MeetingRetrieveUpdateDestroyView.as_view(), name='organize-meeting')
]

