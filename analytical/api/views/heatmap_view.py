from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from analytical.models import HeatMapData
from analytical.api.serializers import HeatMapDataSerializer


class HeatMapDataView(APIView):
    def post(self, request):
        data = request.data  # Gelen verileri alın
        if isinstance(data, list):  # Gelen verilerin bir liste olduğunu kontrol edin
            serializer = HeatMapDataSerializer(data=data, many=True)
            if serializer.is_valid():
                HeatMapData.objects.bulk_create([
                    HeatMapData(**item) for item in serializer.validated_data
                ])
                return Response({"message": "Veriler başarıyla kaydedildi."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Geçersiz veri formatı."}, status=status.HTTP_400_BAD_REQUEST)
