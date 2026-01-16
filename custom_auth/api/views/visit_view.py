from pages.models import PageModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


class LoginPageVisitHandler(APIView):
    def get(self, *args, **kwargs):
        return Response({}, status=HTTP_201_CREATED)

