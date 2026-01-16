from rest_framework import serializers
from pages.models import PageModel, ContextFieldModel
from pages.api.serializers.context_field_serializer import ContextAdminFieldSerializer


class PageSerializer(serializers.ModelSerializer):
    context = serializers.SerializerMethodField()
    view = serializers.SerializerMethodField()

    def get_context(self, instance):
        context_list = instance.context.all()
        context = {}
        for content in context_list:
            context[content.name] = content.field_value
            # content_data = ContextFieldSerializer(instance=content).data
            # context[content_data.get('name')] =
        return context

    def get_view(self, instance):
        return instance.view.count()

    class Meta:
        model = PageModel
        fields = '__all__'


class PageAdminSerializer(serializers.ModelSerializer):
    # context = serializers.SerializerMethodField()
    context = ContextAdminFieldSerializer(many=True)
    view = serializers.SerializerMethodField()

    # def get_context(self, instance):
    #     return [ContextFieldSerializer(instance=context).data for context in instance.context.all()]

    def get_view(self, instance):
        return instance.view.count()

    def update(self, instance, validated_data):
        context = validated_data.get('context')
        validated_data.pop('context')
        for content in context:
            if context_model := ContextFieldModel.objects.filter(name=content.get('name')).first():
                context_model.field_value = content.get('field_value')
                context_model.save()
        return super().update(instance, validated_data)

    class Meta:
        model = PageModel
        fields = '__all__'

