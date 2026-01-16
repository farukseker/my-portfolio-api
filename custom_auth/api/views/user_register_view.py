from rest_framework.generics import CreateAPIView
from custom_auth.api.serializers import UserCreateSerializer


class UserRegisterView(CreateAPIView):
    authentication_classes = []
    serializer_class = UserCreateSerializer

