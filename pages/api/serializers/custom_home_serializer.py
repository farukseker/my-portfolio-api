from rest_framework.serializers import Serializer
from rest_framework.serializers import IntegerField


class CustomHomeSerializer(Serializer):
    ticket = IntegerField()
