from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    LikePost,
    CommentView,
    FollowView,
    UnFollowView,
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts_list"),
    path("posts/<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<uuid:post_id>/like/", LikePost.as_view(), name="like_post"),
    path("posts/<uuid:post_id>/comment/", CommentView.as_view(), name="comment_list"),
    path("follow/<int:user_id>/", FollowView.as_view(), name="follow_user"),
    path("unfollow/<int:user_id>/", UnFollowView.as_view(), name="unfollow_user"),
]
