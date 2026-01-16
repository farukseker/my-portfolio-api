from django.urls import path
from chatwithme.api.views import *

app_name = "chat"

urlpatterns = [
    path('create-chat-room', CreateChatRoomView.as_view(), name='create-chat-room'),
    path('chat-history/<uuid:chat_id>', LoadChatHistoryView.as_view(), name='chat-history'),
    path('<uuid:chat_id>', ChatMessagingView.as_view(), name='chat-with-ai'),
    # feature path('<uuid:chat_id>/<int:message_id>', message update - Delete .as_view(), name='chat-with-ai'),

    path('organize-meeting', MeetingCreateView.as_view(), name='create-meeting'),
    path('organize-meeting/<uuid:meeting_id>', MeetingRetrieveUpdateDestroyView.as_view(), name='organize-meeting'),
]

