from rest_framework.serializers import ModelSerializer
from certificates.api.serializers.certificate_serializer import CertificatesSerializer
from certificates.models import CertificateProviderModel


class CertificatesProviderSerializer(ModelSerializer):
    certificates = CertificatesSerializer(many=True, required=False)
    class Meta:
        model = CertificateProviderModel
        fields: str = '__all__'
