from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("tags", views.TagViewSet, basename="tags")
router.register("posts", views.PostViewSet, basename="posts")

urlpatterns = [path("", include(router.urls))]

app_name = "posts"
