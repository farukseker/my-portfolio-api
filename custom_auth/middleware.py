from django.core.handlers.wsgi import WSGIRequest
from analytical.utils import ViewCountWithRule
from pages.models import PageModel


class OnlyAdminMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        host = request.get_host()
        path = request.path
        print(host)
        print(path)
        print('='*20)
        return self.get_response(request)

    @staticmethod
    def save_a_normal_request(request: WSGIRequest):
        ...
