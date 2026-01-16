from pages.models import PageModel
from rest_framework import serializers


class PageListSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()

    @staticmethod
    def get_view(instance):
        return instance.view.count()

    class Meta:
        model = PageModel
        fields = ('name', 'image', 'title', 'view')

