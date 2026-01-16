from rest_framework import serializers
from game.models import GameInfoModel
from media_manager.api.serializers import MediaSerializer


class GameInfoSerializer(serializers.ModelSerializer):
    banner = MediaSerializer()

    class Meta:
        model = GameInfoModel
        fields: str = '__all__'

