# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404

# Models
from posts.models import Post, Likes


class PostsFeedView(LoginRequiredMixin, ListView):
    """
    Return all published posts
    """
    model = Post
    paginate_by = 5
    ordering = ('-created')
    context_object_name = 'posts'
    template_name = 'posts/feed.html'

    def get_context_data(self, **kwargs):
        """
        Add post's likes to context
        """
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.likes_count = post.likes.count()
            post.is_liking = post.likes.filter(
                user=self.request.user
            ).exists()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Return post detail.
    """
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'post'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        """
        Add post's likes to context
        """
        context = super().get_context_data(**kwargs)
        context['likes_count'] = self.get_object().likes.count()
        context['is_liking'] = self.get_object().likes.filter(
            user=self.request.user
        ).exists()
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Create a new post.
    """
    model = Post
    template_name = 'posts/new.html'
    fields = [
        'title',
        'photo'
    ]

    def form_valid(self, form):
        """
        Validate form.
        """
        form.instance.user = self.request.user
        form.save()
        return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        """
        Return to post's feed.
        """
        return reverse('posts:detail', kwargs={'pk': self.object.pk})
        

class LikeView(LoginRequiredMixin, RedirectView):
    """
    Like or unlike a post.
    """
    pattern_name = 'posts:detail'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        user = self.request.user

        # Check if the user is already liking the post
        like_exists = Likes.objects.filter(
            user=user,
            post=post,
        ).exists()

        if like_exists:
            # If already liking, unlike
            Likes.objects.filter(
                user=user,
                post=post,
            ).delete()
        else:
            # If not liking, like
            Likes.objects.create(
                user=user,
                post=post,
            )

        return super().get_redirect_url(*args, **kwargs)
