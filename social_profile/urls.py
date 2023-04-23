from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("profiles", views.ProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "social_profile"

