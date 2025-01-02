from django.urls import path
from .views import PostListView, PostDetailView, LikePost

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts_list"),
    path("posts/<uuid:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<uuid:post_id>/like/", LikePost.as_view(), name="like_post"),
]
