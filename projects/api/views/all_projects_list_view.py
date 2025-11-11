# views.py
from django.db.models import Count, Prefetch, Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import OrderingFilter, SearchFilter

from projects.api.serializers import ContentListSerializer
from projects.models import ContentModel, ContentCommentModel
from tags.models import TagModel


class AllProjectsListView(ListCreateAPIView):
    serializer_class = ContentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("title", "content_type__name", "tags__name")   # tuple fix
    ordering_fields = ("update", "title", "id")
    authentication_classes = []

    def get_queryset(self):
        qs = (
            ContentModel.objects
            .filter(show=True)
            .only("id", "title", "slug", "update", "language_type", "content_type")  # daralt
            .select_related("content_type")  # FK için tek join (no N+1)
            .annotate(
                view_count=Count("view", distinct=True)  # per-row COUNT(*) N+1'ini öldür
            )
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=TagModel.objects.only("id", "name", "icon_type", "icon"),
                ),
                Prefetch(
                    "comments",
                    queryset=ContentCommentModel.objects.only(
                        "id", "name", "email", "comment", "created"
                    ).order_by("-created"),
                ),
            )
        )

        content_type_param = self.request.query_params.get("content_type")
        if content_type_param:
            qs = qs.filter(content_type__name=content_type_param)

        tags = self.request.query_params.get("tags")
        if tags:
            tag_ids = [t for t in tags.split(",") if t]
            qs = qs.filter(tags__id__in=tag_ids).distinct()

        lang = self.request.query_params.get("lang")
        if lang and lang in ContentModel.LanguageType.values:
            qs = qs.filter(language_type=lang)

        latest_key = next(
            (k for k in ("latest", "limit", "son") if k in self.request.query_params),
            None
        )
        if latest_key:
            raw = self.request.query_params.get(latest_key)
            try:
                n = max(1, min(int(raw), 100))  # hard cap: 100
            except (TypeError, ValueError):
                n = 20  # sensible default
            qs = qs.order_by("-update")[:n]

        return qs