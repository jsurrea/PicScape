# Django
from django.contrib.auth.models import User
from django.db import models

# Utilities
import os


def picture_upload_path(instance, filename):
    """
    Return the path to the profile picture.
    """
    username = instance.user.username
    extension = filename.split('.')[-1]
    unique_filename = f"{username}.{extension}"
    return os.path.join('users', 'pictures', unique_filename)

class Profile(models.Model):
    """
    Profile model.
    Proxy model that extends the base data with other information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)

    biography = models.TextField(blank=True)

    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(
        upload_to=picture_upload_path,
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    posts_count = models.IntegerField(default=0)

    followers = models.IntegerField(default=0)
    
    following = models.IntegerField(default=0)

    def __str__(self):
        """
        Return username.
        """
        return self.user.username
