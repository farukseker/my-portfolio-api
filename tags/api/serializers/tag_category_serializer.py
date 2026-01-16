from rest_framework import serializers
from tags.models import TagCategoryModel
from .tag_serializer import TagSerializer


class TagCategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = TagCategoryModel
        fields: str = '__all__'
