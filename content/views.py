from django.shortcuts import render

from rest_framework import generics
from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.exceptions import ValidationError

from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from core.models import Post, Like, Comment


# Create your views here.
class PostListView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return super().get_queryset().filter(user=self.request.user)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetailView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class LikePost(generics.GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            return Response(
                {"error": "You have already liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LikeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.select_related("user", "post", "parent")
    serializer_class = CommentSerializer
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(post_id=post_id)
        parent_id = self.request.data.get("parent", None)

        if parent_id:
            parent_comment = Comment.objects.get(comment_id=parent_id)
            if parent_comment.post != post:
                return serializer.ValidationError(
                    "Parent comment must belong to the same post."
                )
            serializer.save(user=self.request.user, post=post, parent=parent_comment)
        else:
            serializer.save(user=self.request.user, post=post)
