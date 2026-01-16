from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from analytical.models import ViewModel
from pages.models import PageModel
from contents.models import ContentModel, ContentCommentModel
from message.models import MessageModel
# from game.models import GameVideoModel
from analytical.api.serializers import ViewSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from config.utils import EncryptionService


class UserFlow(APIView):
    permission_classes: list = [IsAuthenticated, IsAdminUser]
    models_with_view_reference: list = PageModel, ContentModel, ContentCommentModel, MessageModel, # GameVideoModel

    def get(self, request, *args, **kwargs):
        time_ranges: dict = {
            'h': timezone.now() - timedelta(hours=1),
            'd': timezone.now() - timedelta(days=1),
            'w': timezone.now() - timedelta(weeks=1),
            'm': timezone.now() - timedelta(weeks=4)
        }
        one_hour_ago = time_ranges.get(request.query_params.get('last'), 'h')
        order = request.query_params.get('order', 'ascend')
        # user_ip = EncryptionService().encrypt_data(kwargs.get('ip'))
        user_ip = kwargs.get('ip')
        views = ViewModel.objects.filter(
            ip_address=user_ip,
            visit_time__gte=one_hour_ago,
        ).order_by('visit_time' if order == 'ascend' else '-visit_time')
        view_data = ViewSerializer(views, many=True).data
        for view in view_data:
            # view['ip_address'] = EncryptionService().decrypt_data(user_ip)
            view['action'] = self.get_view_type(view.get('id'))
        return Response(view_data)

    def get_view_type(self, object_id):
        for model in self.models_with_view_reference:
            if model.objects.filter(view__id=object_id).exists():
                view = model.objects.filter(view__id=object_id).first()
                return {
                    'type': str(view),
                    'title': view.title,
                }
        return {
            'type': 'unknown',
            'title': 'unknown action',
        }


