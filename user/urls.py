from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet, basename="users")

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.CreateTokenView.as_view(), name="login"),
    path("logout/", views.DeleteTokenView.as_view(), name="logout"),
    path("", include(router.urls)),
]

app_name = "user"
