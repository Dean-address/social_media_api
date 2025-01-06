from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomUserSerializer
from rest_framework.parsers import FormParser, MultiPartParser


class ActivateUser(UserViewSet):
    # To aciivate user account
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    parser_classes = (FormParser, MultiPartParser)
