# Django
from django.urls import path

# View
from users import views

urlpatterns = [

    # Management
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route='signup/',
        view=views.SignupView.as_view(),
        name='signup'
    ),
    path(
        route='me/',
        view=views.ProfileUpdateView.as_view(),
        name='profile'
    ),

    # Profiles
    path(
        route='u/<str:username>/',
        view=views.ProfileDetailView.as_view(),
        name='detail'
    ),
    path(
        route='f/<str:username>/',
        view=views.FollowView.as_view(),
        name='follow'
    ),

]