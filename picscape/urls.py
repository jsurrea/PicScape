# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# Views
from . import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.RootRedirectView.as_view(), name='root_redirect'),
    path('', include(('posts.urls','posts'), namespace ='posts')),
    path('', include(('users.urls','users'), namespace ='users')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
