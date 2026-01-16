from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from tags.api.serializers import TagCategorySerializer
from tags import models


# class AllTagsListView(APIView):
#     authentication_classes = []
#
#     def get(self, request, *args, **kwargs):
#         model_names: list = [name for name in dir(models) if name.endswith('Model')]
#         result: dict = {}
#
#         for model_name in model_names:
#             model_class = getattr(models, model_name)
#             serializer_class_name: str = model_name.replace('Model', 'Serializer')
#
#             if hasattr(tags_serializers, serializer_class_name):
#                 serializer_class = getattr(tags_serializers, serializer_class_name)
#                 instances: model_class = model_class.objects.all()
#                 serialized_data = serializer_class(instance=instances, many=True).data
#                 result[model_name]: dict = serialized_data
#
#         return Response(result)

class AllTagsListView(ListAPIView):
    serializer_class = TagCategorySerializer
    queryset = models.TagCategoryModel.objects.all()

