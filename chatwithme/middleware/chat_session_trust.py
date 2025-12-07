from django.core.handlers.wsgi import WSGIRequest
from django.urls import ResolverMatch
from rest_framework.exceptions import ValidationError
from analytical.utils import get_client_ip
from chatwithme.models import ChatRoom
import hashlib


class ChatSessionTrustMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.trust_need_origins: list[str] = [
            "chat-history",
            "chat"
        ]

    def is_request_in_allowed_paths(self, request: WSGIRequest) -> bool:
        for path in self.trust_need_origins:
            if path in request.path:
                return True
        return False

    @staticmethod
    def hash_obj(text):
        h = hashlib.new("sha256")
        h.update(str(text).encode("utf-8"))
        return h.hexdigest()

    @staticmethod
    def get_chat_id_from_request(request: WSGIRequest) -> str | None:
        if hasattr(request, 'resolver_match') and isinstance(request.resolver_match, ResolverMatch):
            return request.resolver_match.kwargs.get("chat_id", None)
        return None

    def __call__(self, request: WSGIRequest):
        response = self.get_response(request)
        client_ip: str = get_client_ip(request)
        chat_id: str | None = self.get_chat_id_from_request(request)
        if all([
            chat_id,
            client_ip,
            request.get_full_path().startswith('/api/chat/'),
            self.is_request_in_allowed_paths(request)
        ]):
            chat_room = ChatRoom.objects.filter(session_id=chat_id).first()
            original_hash = self.hash_obj(str(chat_room.session_id) + str(client_ip))
            test_hash = self.hash_obj(str(chat_id) + str(client_ip))
            if original_hash != test_hash:
                raise ValidationError("trusted session ids don't match")
        return response
