from rest_framework.generics import ListAPIView
from certificates.models import CertificateProviderModel
from certificates.api.serializers import CertificatesProviderSerializer


class CertificatesListView(ListAPIView):
    queryset = CertificateProviderModel.objects.all()
    serializer_class = CertificatesProviderSerializer

