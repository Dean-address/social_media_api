from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import os
import uuid
from cloudinary.models import CloudinaryField

from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **other_fields):
        """Create and save a new user"""
        if not email:
            return ValueError("User must have an email address.")
        user = self.model(
            email=self.normalize_email(email), username=username, **other_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, username=None):
        """Create and save a superuser"""
        user = self.create_user(email, password, username="")
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


def profile_image_file_path(instance, filename):

    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "profiles", filename)


class UserProfile(models.Model):
    """Profile for a user"""

    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="userprofile"
    )
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    other_names = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    telephone = models.CharField(max_length=255, blank=True)
    gender = models.CharField(
        max_length=255,
        blank=True,
        choices=[
            ("MALE", "MALE"),
            ("FEMALE", "FEMALE"),
        ],
    )
    image = models.ImageField(null=True, blank=True, upload_to=profile_image_file_path)

    def __str__(self):
        return self.user.username


def post_image_file_path(instance, filename):

    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("post", "images", filename)


def post_video_file_path(instance, filename):

    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("post", "videos", filename)


class Post(models.Model):
    """Post model for user"""

    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    image = CloudinaryField("image", null=True, blank=True)
    video = CloudinaryField(resource_type="video", null=True, blank=True)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        return f"https://res.cloudinary.com/dobvp4toj/{self.image}"

    @property
    def video_url(self):
        return f"https://res.cloudinary.com/dobvp4toj/{self.video}"

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class Like(models.Model):
    """Like model for user"""

    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="likes_user"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} like Post {self.post.post_id}"


class Comment(models.Model):
    """Comment model for user"""

    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.post_id}"

    @property
    def is_reply(self):
        return self.parent is not None


class Follow(models.Model):
    """Follow model for user"""

    follow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
