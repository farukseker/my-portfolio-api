from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import OTPTestView, CustomTokenObtainPairView, UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "auth"

urlpatterns = [
    path('otp_test/', OTPTestView.as_view()),
    # path('otp'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterView.as_view(), name='register')
]

