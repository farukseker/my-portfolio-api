from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from rest_framework import status

from chatwithme.api.views.start_chat_with_llm import CreateChatRoomView
from chatwithme.api.views.load_chat_history import LoadChatHistoryView
from chatwithme.api.views.chat_messagin import ChatMessagingView
from chatwithme.models import ChatRoom, ChatLog


class ChatUrlsResolveTests(TestCase):
    def test_create_chat_room_url_resolves(self):
        url = reverse("api:chat:create-chat-room")
        resolver = resolve(url)
        self.assertIs(resolver.func.view_class, CreateChatRoomView)

    def test_chat_history_url_resolves(self):
        fake_uuid = "12345678-1234-1234-1234-1234567890ab"
        url = reverse("api:chat:chat-history", kwargs={"chat_id": fake_uuid})
        resolver = resolve(url)
        self.assertIs(resolver.func.view_class, LoadChatHistoryView)

    def test_chat_with_ai_url_resolves(self):
        fake_uuid = "12345678-1234-1234-1234-1234567890ab"
        url = reverse("api:chat:chat-with-ai", kwargs={"chat_id": fake_uuid})
        resolver = resolve(url)
        self.assertIs(resolver.func.view_class, ChatMessagingView)


class ChatApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_chat_room_returns_room_id(self):
        url = reverse("api:chat:create-chat-room")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("room_id", response.data)
        self.assertTrue(
            ChatRoom.objects.filter(session_id=response.data["room_id"]).exists()
        )

    def test_load_chat_history_returns_logs(self):
        room = ChatRoom.objects.create()
        # Signal automatically creates 1 ChatLog when ChatRoom is created
        # So we expect 3 logs total: 1 from signal + 2 we create manually
        ChatLog.objects.create(room=room, message="hi", type="human")
        ChatLog.objects.create(room=room, message="hello", type="ai")

        url = reverse("api:chat:chat-history", kwargs={"chat_id": room.session_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Signal creates 1 log + 2 manual logs = 3 total
        self.assertEqual(len(response.data), 3)
