# Generated by Django 4.2 on 2023-04-21 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="profiles/avatars/%Y/%m/%d/",
                    ),
                ),
                ("first_name", models.CharField(max_length=63)),
                ("last_name", models.CharField(max_length=63)),
                ("user_name", models.CharField(max_length=63)),
                ("birth_day", models.DateField(blank=True, null=True)),
                ("about", models.TextField(max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
