from rest_framework import serializers
from analytical.models import HeatMapData


class HeatMapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatMapData
        fields = ['x', 'y', 'timestamp', 'view']
