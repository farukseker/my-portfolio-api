from rest_framework.generics import CreateAPIView
from certificates.api.serializers import CertificatesProviderSerializer
from certificates.models import CertificateProviderModel


class CertificateProviderCreateView(CreateAPIView):
    serializer_class = CertificatesProviderSerializer
    queryset = CertificateProviderModel.objects.all()

