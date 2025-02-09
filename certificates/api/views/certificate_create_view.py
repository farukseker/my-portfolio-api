from rest_framework.generics import CreateAPIView
from certificates.api.serializers import CertificatesSerializer
from certificates.models import CertificateModel


class CertificateCreateView(CreateAPIView):
    serializer_class = CertificatesSerializer
    queryset = CertificateModel.objects.all()

