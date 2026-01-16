from rest_framework import serializers
from .project_serializer import ContentSerializer


class CustomBLogContentSerializer(serializers.Serializer):
    contents = ContentSerializer(many=True)
    # trends = ContentSerializer(many=True)
    trends = serializers.SerializerMethodField()
    featured = ContentSerializer(many=True)

    @staticmethod
    def get_trends(instance):
        return [{'title': trend.title, 'slug': trend.slug} for trend in instance.get('trends', [])]

    '''
    @feured objeleri contente var ise silinecek | opts
    '''