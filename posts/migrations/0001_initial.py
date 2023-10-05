# Generated by Django 4.2.3 on 2023-10-05 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=255)),
                (
                    "photo",
                    models.ImageField(upload_to=posts.models.picture_upload_path),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("likes", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
