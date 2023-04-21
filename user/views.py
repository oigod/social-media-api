from django.contrib.auth import logout
from django.db import transaction
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView


from user.serializers import UserSerializer, AuthTokenSerializer


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
