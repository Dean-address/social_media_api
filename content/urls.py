from django.urls import path
from .views import PostListView, PostDetailView, LikePost, CommentView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts_list"),
    path("posts/<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<uuid:post_id>/like/", LikePost.as_view(), name="like_post"),
    path("posts/<uuid:post_id>/comment/", CommentView.as_view(), name="comment_list"),
]
