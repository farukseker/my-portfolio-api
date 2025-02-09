from django.urls import path, include
from certificates.api.views import CertificatesListView, CertificateCreateView, CertificateProviderCreateView


app_name: str = "certificates"

urlpatterns: list[path] = [
    path('provider/create/', CertificateProviderCreateView.as_view()),
    # slug CURD path('<slug:slug>/', CertificateProviderCreateView.as_view()),
    path('', CertificatesListView.as_view())
]
