# Django
from django.urls import path

# Views
from posts import views

urlpatterns = [

    path(
        route='feed/',
        view=views.PostsFeedView.as_view(),
        name='feed'
    ),
    path(
        route='posts/<int:pk>',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),
    path(
        route='posts/new/',
        view=views.CreatePostView.as_view(),
        name='create'
    ),
  
]