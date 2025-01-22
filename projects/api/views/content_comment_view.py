from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from projects.api.serializers import ContentCommentCreateSerializer
from projects.models import ContentModel, ContentCommentModel
from game.models import GameVideoModel


class CreateCommentView(CreateAPIView):
    model = ContentCommentModel
    serializer_class = ContentCommentCreateSerializer
    authentication_classes = []
    content_models: list = [
        ContentModel,
        GameVideoModel,
    ]

    def post(self, request, *args, **kwargs):
        content_slug = kwargs.get('slug', None)
        content = self.get_multi_content_models(slug=content_slug, show=True)
        if not content:
            raise Http404("No matches the given query.")
        content_comment_serializer: ContentCommentCreateSerializer = self.get_serializer(data=request.data)
        if content_comment_serializer.is_valid():
            new_comment = content_comment_serializer.save()
            content.comments.add(new_comment)
            return Response(content_comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(content_comment_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_multi_content_models(self, **kwargs):
        def query(_model, **_kwargs):
            if _ := _model.objects.filter(**_kwargs):
                return _.first()

        for model in self.content_models:
            if result := query(model, **kwargs):
                return result
