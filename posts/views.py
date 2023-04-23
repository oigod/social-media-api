from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts import serializers
from posts.models import Tag, Post
from posts.permissions import IsOwnerOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    lookup_field = "pk"

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        tags = self.request.query_params.get("tags")
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.distinct()

    @action(methods=["GET"], detail=False, url_path="my-posts")
    def my_posts(self, request):
        queryset = self.queryset.filter(author=request.user.pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="my-following-posts")
    def my_following_posts(self, request):
        queryset = self.queryset.filter(
            author__in=request.user.followers.all()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsOwnerOrReadOnly, IsAuthenticated]

        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filtering by tags id (ex. ?tags=1,2,3)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
