from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta
from django.utils.timezone import now
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from chatwithme.models import ChatHistory
from chatwithme.api.serializers import ChatHistorySerializer
import hashlib


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def is_ip_banned(ip):
    return cache.get(f"banned:{ip}") is not None


MAX_MESSAGES_PER_HOUR = 100


def is_rate_limited(ip):
    one_hour_ago = now() - timedelta(hours=1)
    count = ChatHistory.objects.filter(ip_address=ip, timestamp__gte=one_hour_ago).count()
    return count >= MAX_MESSAGES_PER_HOUR


def track_uuid_attempt(ip, session_id):
    key = f"uuid_attempts:{ip}"
    attempts = cache.get(key)

    if attempts is None:
        attempts = set()

    # UUID hashle ki hafıza dostu olsun
    hashed_uuid = hashlib.sha256(session_id.encode()).hexdigest()
    attempts.add(hashed_uuid)
    cache.set(key, attempts, timeout=3600)

    if len(attempts) > 10:
        cache.set(f"banned:{ip}", True, timeout=3600)
        return False
    return True


class ChatHistoryView(APIView):
    def post(self, request):
        session_id = request.headers.get("X-Session-ID")
        ip = get_client_ip(request)

        if is_ip_banned(ip):
            return Response({"error": "IP banned"}, status=429)

        if not session_id:
            return Response({"error": "Missing session ID"}, status=400)

        if not track_uuid_attempt(ip, session_id):
            return Response({"error": "Too many session IDs"}, status=429)

        if is_rate_limited(ip):
            return Response({"error": "Rate limit exceeded (max 100 messages/hour)"}, status=429)

        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"error": "Empty message"}, status=400)

        llm_response = "LLM cevabı buraya gelecek."

        ChatHistory.objects.create(
            session_id=session_id,
            message=user_message,
            response=llm_response,
            is_user_message=True,
            ip_address=ip
        )

        return Response({"response": llm_response})
