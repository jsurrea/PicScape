# Django
from django.contrib import admin

# Models
from users.models import Profile, Follows

admin.site.register(Profile)
admin.site.register(Follows)
