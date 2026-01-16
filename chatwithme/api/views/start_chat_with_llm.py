from rest_framework.response import Response
from rest_framework.views import APIView
from chatwithme.models import ChatRoom
from rest_framework.exceptions import NotAcceptable
from analytical.utils import get_client_ip
import hashlib

class CreateChatRoomView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        if client_ip := get_client_ip(request):
            chat_room = ChatRoom.objects.create()

            h = hashlib.new('SHA256')
            h.update(bytes(str(chat_room.session_id) + str(client_ip), encoding='utf-8'))

            chat_room.hash_stamp = h.hexdigest()
            chat_room.save()
            return Response({'room_id': chat_room.session_id})
        raise NotAcceptable
