from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from social_profile.models import Profile
from social_profile.permissions import IsOwnerOrReadOnly
from social_profile.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        queryset = self.queryset

        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(user_name__icontains=username)

        return queryset

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsAuthenticated, IsOwnerOrReadOnly]

        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type={"type": "str"},
                description="Filtering by username string (ex. ?username=John)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)