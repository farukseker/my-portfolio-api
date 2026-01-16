from chatwithme.models import ChatLog
from rest_framework import serializers


class ChatLogHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLog
        # fields: str = '__all__'
        read_only_fields: str = [
            'type',
            'timestamp',
        ]
        exclude = 'room',