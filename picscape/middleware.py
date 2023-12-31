# Django
from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    """
    Ensure every user that is interacting with the platform
    has their profile picture and biography.
    """

    def __init__(self, get_response):
        """
        Middleware initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view is called.
        """
        if request.user.is_staff and not request.path.startswith(reverse('admin:index')):
            return redirect(reverse('admin:index'))
        if (
            request.user.is_anonymous
            or request.user.is_anonymous
            or request.user.is_staff
            or request.user.profile.picture and 
            request.user.profile.biography
            or request.path == reverse('users:profile')
            or request.path == reverse('users:logout')
        ):
            response = self.get_response(request)
            return response
        return redirect('users:profile')
