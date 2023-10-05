# Django
from django.db import models
from django.contrib.auth.models import User

# Utilities
from uuid import uuid4
import os


def picture_upload_path(instance, filename):
    """
    Return the path to the post picture.
    """
    username = instance.user.username
    extension = filename.split('.')[-1]
    unique_filename = f"{username}-{uuid4()}.{extension}"
    return os.path.join('posts', 'photos', unique_filename)


class Post(models.Model):
    """
    Post model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)

    photo = models.ImageField(upload_to=picture_upload_path)

    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    likes = models.IntegerField(default=0)

    def __str__(self):
        """
        Return title and username.
        """
        return '{} by @{}'.format(self.title, self.user.username)
        