from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserCreateSerializer):
    follower_list = serializers.SerializerMethodField()
    following_list = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "user_id",
            "email",
            "username",
            "password",
            "follower_count",
            "following_count",
            "follower_list",
            "following_list",
        )

    def get_follower_list(self, obj):
        request = self.context.get("request")
        return [
            request.build_absolute_uri(
                reverse("customuser-detail", kwargs={"id": user.following.id})
            )
            for user in obj.following.all()
        ]

    def get_following_list(self, obj):
        request = self.context.get("request")

        return [
            request.build_absolute_uri(
                reverse("customuser-detail", kwargs={"id": user.follower.id})
            )
            for user in obj.followers.all()
        ]

    def get_follower_count(self, obj):
        return obj.following.count()

    def get_following_count(self, obj):
        return obj.followers.count()
