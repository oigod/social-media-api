from rest_framework import serializers

from . import models


class ProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(
        max_length=255, source="get_full_name", read_only=True
    )

    class Meta:
        model = models.Profile
        fields = ("id", "avatar", "user_name", "birth_day", "fullname", "user")
