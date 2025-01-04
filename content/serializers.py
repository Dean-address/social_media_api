from rest_framework import serializers
from core.models import Post, Like, Comment


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ["like_id", "user", "post", "created_at"]
        read_only_fields = ["like_id", "user", "post", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "user",
            "post",
            "parent",
            "content",
            "created_at",
            "replies",
        ]
        read_only_fields = ["comment_id", "user", "post", "created_at"]

    def get_replies(self, obj):
        if obj.replies.exists():

            return CommentSerializer(
                obj.replies.all(), many=True, context=self.context
            ).data

        return []


class PostSerializer(serializers.ModelSerializer):

    image_url = serializers.ReadOnlyField()
    video_url = serializers.ReadOnlyField()
    likes_count = serializers.SerializerMethodField()
    likes_by = LikeSerializer(many=True, read_only=True, source="likes")
    comments = CommentSerializer(many=True, read_only=True)

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
            "likes_count",
            "likes_by",
            "comments",
        ]
        read_only_fields = ["post_id", "user", "created_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(instance.comments.filter(parent=None))
        for key, value in representation.items():
            if key == "comments":
                comments = [comment for comment in value if comment["parent"] is None]
                representation[key] = comments
        representation.pop("image")
        representation.pop("video")
        return representation

    def get_likes_count(self, obj):
        return obj.likes.count()
