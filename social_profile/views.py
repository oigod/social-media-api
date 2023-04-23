from rest_framework import viewsets

from social_profile.models import Profile
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
