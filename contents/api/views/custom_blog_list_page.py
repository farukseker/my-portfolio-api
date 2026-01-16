from rest_framework.generics import ListAPIView
from contents.api.serializers import CustomBLogContentSerializer
from contents.models import ContentModel
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class CustomBlogContentView(ListAPIView):
    serializer_class = CustomBLogContentSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        match self.request.query_params.get('order_by', 'ascending'):
            case 'ascending':
                order_param = 'created'
            case 'descending':
                order_param = '-created'
            case _:
                order_param = 'created'

        queryset = ContentModel.objects.filter(show=True, content_type__name='blog')

        data = {
            'contents': queryset.order_by(order_param),
            'trends': queryset.order_by('-view')[:4],
            'featured': queryset.filter(is_featured=True),
        }
        serializer = self.serializer_class(data)

        return Response(serializer.data)
