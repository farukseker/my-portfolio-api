from tags.models import TagModel
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class TagSerializer(ModelSerializer):
    category = SerializerMethodField(read_only=True)

    @staticmethod
    def get_category(obj):
        return obj.category.name if obj.category else None

    class Meta:
        model = TagModel
        fields: str = '__all__'

