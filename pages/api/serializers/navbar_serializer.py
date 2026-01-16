from rest_framework import serializers
from pages.models import NavbarModel, NavbarItemModel


class NavbarItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarItemModel
        fields = '__all__'


class NavbarSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    @staticmethod
    def get_items(instance):
        return {position: [NavbarItemSerializer(navbar_item).data for navbar_item in
                           instance.items.filter(navbar_item_position=position)] for position in
                ['start', 'center', 'end']}

    class Meta:
        model = NavbarModel
        fields = '__all__'

