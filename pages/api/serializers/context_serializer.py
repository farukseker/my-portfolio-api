from rest_framework import serializers
from pages.models import ContextModel


class ContextSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContextModel
        fields = '__all__'

