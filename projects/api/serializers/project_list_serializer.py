from django.utils import timesince
from rest_framework import serializers
from projects.models import ContentModel
from .project_serializer import ContentSerializer, ContentCommentSerializer
from typing import List, Dict
#
# @staticmethod
# def get_word_count(instance):
#     return len(instance.text.split(' ')) if instance.text else 0


class ContentListSerializer(ContentSerializer):
    update = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    humanize_date = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    comments = ContentCommentSerializer(many=True)

    @staticmethod
    def get_comments(obj) -> List:
        return []

    @staticmethod
    def get_humanize_date(obj) -> Dict:
        return {
            'create': timesince.timesince(obj.created),
            'update': timesince.timesince(obj.update),
        }

    class Meta:
        model = ContentModel
        exclude: tuple = 'embedding',
        # fields: str = '__all__'
