from rest_framework import serializers
from chatwithme.models import MeetingModel


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model: MeetingModel = MeetingModel
        # fields: str = '__all__'
        exclude: tuple[str] = ('id',)
