from projects.models import ContentCommentModel
from rest_framework import serializers
from analytical.utils import ViewCountWithRule


class ContentCommentCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if self.context:
            counter = ViewCountWithRule(None, self.context['request'])
            validated_data['view'] = counter.create_view()
        return super().create(validated_data)

    class Meta:
        model = ContentCommentModel
        exclude: tuple = 'view',
