from chatwithme.models import ChatHistory
from rest_framework import serializers


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields: str = '__all__'
