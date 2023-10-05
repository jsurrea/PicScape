# Django
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

# Models
from posts.models import Post


class PostsFeedView(LoginRequiredMixin, ListView):
    """
    Return all published posts
    """
    model = Post
    paginate_by = 5
    ordering = ('-created')
    context_object_name = 'posts'
    template_name = 'posts/feed.html'


class PostDetailView(LoginRequiredMixin, DetailView):
    """
    Return post detail.
    """
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'post'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'


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
        
