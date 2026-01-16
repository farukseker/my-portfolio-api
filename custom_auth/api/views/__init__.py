from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from custom_auth.api.permissions import OtpAllow
from custom_auth.models import OTPModel
from rest_framework_simplejwt.views import TokenObtainPairView
from custom_auth.api.serializers import CustomTokenObtainPairSerializer


class OTPView(APIView):
    def post(self, request, *args, **kwargs):

        print(self)
        print(self.headers)
        print(request)
        print(args)
        print(kwargs)
        # request.session.__setitem__('session_authorization', True)

        return Response({}, status=200)


class OTPTestView(APIView):
    permission_classes = [
        OtpAllow
    ]

    def get(self, request, *args, **kwargs):
        return Response({})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# split


class UserRegisterView(CreateAPIView):
    ...


from .user_register_view import UserRegisterView

