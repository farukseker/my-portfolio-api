from rest_framework import serializers
from ...models import ContextFieldModel


class ContextFieldSerializer(serializers.ModelSerializer):
    field_value = serializers.SerializerMethodField()

    def get_field_value(self, instance):
        return instance.get_field_value()

    class Meta:
        model = ContextFieldModel
        fields = '__all__'


class ContextAdminFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextFieldModel
        fields = '__all__'
