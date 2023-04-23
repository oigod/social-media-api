from django.contrib.auth import logout, get_user_model
from django.db import transaction
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView

from social_profile.models import User
from user.serializers import UserSerializer, AuthTokenSerializer, FollowerSerializer, UserListSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ObtainAuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )


class DeleteTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        with transaction.atomic():
            token = request.auth
            token_obj = get_object_or_404(Token, key=token)
            token_obj.delete()
            logout(request)
            return Response(status=status.HTTP_200_OK)


class CreateTokenView(ObtainAuthTokenView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer

    @action(detail=True, methods=["POST"])
    def follow(self, request, pk=None):
        followee = self.get_object()
        follower = request.user
        follower.followers.add(followee)
        follower.save()
        serializer = self.get_serializer(follower)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"])
    def unfollow(self, request, pk=None):
        followee = self.get_object()
        follower = request.user
        follower.followers.remove(followee)
        follower.save()
        serializer = self.get_serializer(follower)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="followings")
    def followings(self, request):
        user = request.user
        serializer = UserListSerializer(user.followers.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="followers")
    def followers(self, request):
        user = request.user
        serializer = UserListSerializer(get_user_model().objects.filter(followers__id__in=[user.pk]), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
