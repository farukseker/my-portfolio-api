from rest_framework import serializers
from game.models import GameVideoModel
from game.api.serializers.music_info_serializer import MusicInfoSerializer
from game.api.serializers.game_info_serializer import GameInfoSerializer
from media_manager.api.serializers import MediaSerializer
from projects.api.serializers import ContentCommentSerializer


class GameVideoSerializer(serializers.ModelSerializer):
    seo_image_url = serializers.CharField()
    video = MediaSerializer()
    view = serializers.SerializerMethodField()
    music = MusicInfoSerializer()
    game = GameInfoSerializer()
    comments = ContentCommentSerializer(many=True, required=False)

    @staticmethod
    def get_view(obj):
        return obj.get_view().count()

    class Meta:
        model = GameVideoModel
        fields: str = '__all__'

