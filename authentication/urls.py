from django.urls import path
from .views import ActivateUser


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

app_name = "authentication"

urlpatterns = [
    path(
        "activate/<str:uid>/<str:token>",
        ActivateUser.as_view({"get": "activation"}),
        name="activation",
    ),
]
