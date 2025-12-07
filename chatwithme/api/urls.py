from django.urls import path
from chatwithme.api.views import *
import uuid

app_name = "chat"

urlpatterns = [
    path('create-chat-room', CreateChatRoomView.as_view(), name='create-chat-room'),
    # path('chat/<str:chat_id>', ),
    path('chat-history/<uuid:chat_id>', LoadChatHistoryView.as_view(), name='chat-history'),
    path('organize-meeting', MeetingCreateView.as_view(), name='create-meeting'),
    path('organize-meeting/<uuid:meeting_id>', MeetingRetrieveUpdateDestroyView.as_view(), name='organize-meeting')
]

