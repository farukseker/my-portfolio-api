from rest_framework.generics import CreateAPIView
from message.models import MessageModel
from message.api.serializers import MessageCreateSerializer


class CreateMessageView(CreateAPIView):
    model = MessageModel
    serializer_class = MessageCreateSerializer
    authentication_classes = []
