from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, related_name="profile", on_delete=models.CASCADE
    )
    avatar = models.ImageField(
        blank=True, null=True, upload_to="profiles/avatars/%Y/%m/%d/"
    )
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    user_name = models.CharField(max_length=63)
    birth_day = models.DateField(blank=True, null=True)
    about = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.user_name
