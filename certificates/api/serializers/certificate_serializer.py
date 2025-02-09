from rest_framework.serializers import ModelSerializer
from certificates.models import CertificateModel


class CertificatesSerializer(ModelSerializer):

    class Meta:
        model = CertificateModel
        fields: str = '__all__'
