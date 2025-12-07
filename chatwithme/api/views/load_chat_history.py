from rest_framework.generics import ListAPIView
from chatwithme.models import ChatRoom, ChatLog
from chatwithme.api.serializers import ChatLogHistorySerializer


class LoadChatHistoryView(ListAPIView):
    permission_classes = []

    serializer_class = ChatLogHistorySerializer

    def get_queryset(self):
        if chat_id := self.kwargs.get('chat_id', None):
            chat_room = ChatRoom.objects.filter(session_id=chat_id).first()
            return ChatLog.objects.filter(room=chat_room).all()
