# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import DetailView, FormView, UpdateView, RedirectView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile, Follows

# Forms
from users.forms import SignupForm


class LoginView(auth_views.LoginView):
    """
    Users login view.
    """
    template_name = 'users/login.html'
    next_page = 'posts:feed'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """
    Users logout view.
    """
    next_page = 'users:login'


class SignupView(FormView):
    """
    Users sign up view.
    """
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        """
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Return to login page.
        """
        return reverse('users:login')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update profile view.
    """
    template_name = 'users/profile.html'
    model = Profile
    fields = [
        'website', 
        'biography', 
        'phone_number', 
        'picture'
    ]

    def get_object(self):
        """
        Return user's profile.
        """
        return self.request.user.profile

    def get_success_url(self):
        """
        Return to user's profile.
        """
        username = self.object.user.username
        return reverse(
            'users:detail', 
            kwargs={
                'username': username,
            }
        )


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    User detail view.
    """
    template_name = 'users/detail.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username' 
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """
        Add user's posts to context
        """
        context = super().get_context_data(**kwargs)
        followee = self.get_object()
        follower = self.request.user

        context['is_following'] = Follows.objects.filter(
            follower=follower,
            followee=followee,
        ).exists()

        context['posts'] = self.get_object().posts.all()
        context['posts_count'] = self.get_object().posts.count()
        context['followers_count'] = self.get_object().followers.count()
        context['following_count'] = self.get_object().following.count()

        return context


class FollowView(LoginRequiredMixin, RedirectView):
    """
    Follow or unfollow a user.
    """
    pattern_name = 'users:detail'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        username = kwargs['username']
        followee = get_object_or_404(User, username=username)
        follower = self.request.user

        # Check if the user is already following
        follow_exists = Follows.objects.filter(
            follower=follower,
            followee=followee,
        ).exists()

        if follow_exists:
            # If already following, unfollow
            Follows.objects.filter(
                follower=follower,
                followee=followee,
            ).delete()
        else:
            # If not following, follow
            Follows.objects.create(
                follower=follower,
                followee=followee,
            )

        return super().get_redirect_url(*args, **kwargs)
