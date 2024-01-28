from tags.models import ToolModel
from rest_framework.serializers import ModelSerializer


class ToolSerializer(ModelSerializer):
    class Meta:
        model = ToolModel
        fields: str = '__all__'

