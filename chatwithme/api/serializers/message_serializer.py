from rest_framework import serializers


class HumanMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
