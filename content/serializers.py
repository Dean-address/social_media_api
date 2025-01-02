from rest_framework import serializers
from core.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    video_url = serializers.ReadOnlyField()
    # likes_count = serializers.SerializerMethodField()
    # is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "post_id",
            "user",
            "text",
            "image",
            "image_url",
            "video",
            "video_url",
            "caption",
            "created_at",
        ]
        read_only_fields = ["post_id", "user", "created_at"]

    # def create(self, validated_data):
    #     request = self.context.get("request")
    #     validated_data["user"] = request.user
    #     return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("image")
        representation.pop("video")
        return representation

    # def get_likes_count(self, obj):
    #     return obj.likes.count()

    # def get_is_liked(self, obj):
    #     request = self.context.get("request")
    #     return obj.likes.filter(user=request.user).exists()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["like_id", "user", "post", "created_at"]
        read_only_fields = ["like_id", "user", "post", "created_at"]
