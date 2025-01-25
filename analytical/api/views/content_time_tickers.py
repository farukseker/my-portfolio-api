from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from analytical.models import ViewModel
from analytical.utils import get_client_ip


class ContentTimeTick(APIView):
    lookup_field = 'pk'
    permission_classes = []
    authentication_classes = []

    def post(self, *args, **kwargs):
        request_ip = get_client_ip(self.request)
        pk = kwargs.get('pk', None)
        if view := ViewModel.objects.filter(ip_address=request_ip, pk=pk).first():
            view.tick()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
