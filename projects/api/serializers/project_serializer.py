from rest_framework import serializers

from .comment_serializer import ContentCommentSerializer
from projects.models import ContentModel
from tags.api.serializers.tag_serializer import TagSerializer
from tags.models import TagModel


class ContentSerializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField(required=False, read_only=True)
    ticket = serializers.SerializerMethodField(required=False, read_only=True)
    comments = ContentCommentSerializer(many=True, required=False)
    # tags = TagSerializer(many=True, required=False)
    view = serializers.SerializerMethodField()

    @staticmethod
    def get_ticket(instance):

        if hasattr(instance, 'ticket'):
            return getattr(instance, 'ticket')
        return None

    @staticmethod
    def get_word_count(instance):
        return len(instance.text.split(' ')) if instance.text else 0

    @staticmethod
    def get_view(instance):
        return instance.get_view().count()

    class Meta:
        model = ContentModel
        fields = '__all__'
        # exclude: tuple = 'show',

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        # comments_data = validated_data.pop('comments', [])

        instance = ContentModel.objects.create(**validated_data)

        for tag_data in tags_data:
            if tag := TagModel.objects.filter(pk=tag_data['pk']):
                instance.tags.add(tag)
            else:
                _tag_data = tag_data
                _tag_data.pop('pk')
                tag = TagModel.objects.create(**_tag_data)

        return instance

    def update(self, instance, validated_data):

        validated_data.pop('word_count', None)
        validated_data.pop('comments', None)
        validated_data.pop('view', None)
        validated_data.pop('ticket', None)

        if instance is None:
            return super().create(validated_data)

        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        for tag_data in tags_data:
            tag = TagModel.objects.get(name=tag_data['name'])
            instance.tags.add(tag)
        instance.save()
        return instance
