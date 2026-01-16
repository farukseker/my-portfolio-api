from rest_framework import serializers
from analytical.api.serializers import ViewSerializer
from analytical.utils import ViewCountWithRule
from message.models import MessageModel
from config.settings.base import CUSTOM_LOGGER


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields: tuple = 'name', 'email', 'message'
        extra_kwargs = {'view': {'write_only': True}}

    def create(self, validated_data):
        counter = ViewCountWithRule(None, self.context['request'])
        view = counter.create_view()
        validated_data['view'] = view
        message = super(MessageCreateSerializer, self).create(validated_data)
        CUSTOM_LOGGER.construct(
            title=f'New Message From [{message.email}]',
            level='verbose',
            metadata={
                "name": message.name,
                "email": message.email,
                "ticket": view.pk,
            },
            description=f'Message: {message.message}'
        )
        CUSTOM_LOGGER.send()
        return message


class MessageReaderSerializer(serializers.ModelSerializer):
    view = ViewSerializer()

    class Meta:
        model = MessageModel
        fields: str = '__all__'

