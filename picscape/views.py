from django.views.generic import RedirectView

class RootRedirectView(RedirectView):
    """
    Redirect the root URL to the 'feed' view.
    """
    pattern_name = 'posts:feed'
    permanent = False
