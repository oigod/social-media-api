from django.urls import path
from rest_framework.authtoken import views

from . import views

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.CreateTokenView.as_view(), name="login"),
    path("logout/", views.DeleteTokenView.as_view(), name="logout"),
]

app_name = "user"
