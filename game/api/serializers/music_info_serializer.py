from rest_framework import serializers
from game.models import MusicInfoModel


class MusicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicInfoModel
        fields: str = '__all__'

