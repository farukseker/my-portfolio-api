from rest_framework import serializers
from .game_video_serializer import GameVideoSerializer
from game.models import GameVideoModel


class GameVideoListSerializer(GameVideoSerializer):
    video = None


