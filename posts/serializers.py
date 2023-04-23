from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class TagShortDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ("name",)


class PostSerializer(serializers.ModelSerializer):
    tags = TagShortDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = (
            "id",
            "title",
            "text",
            "image",
            "tags",
            "author",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
        )
