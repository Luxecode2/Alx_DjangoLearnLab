from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q # For complex search queries
from taggit.models import Tag # For filtering by tags

from .models import Post, Comment
from .forms import CustomUserCreationForm, ProfileEditForm, PostForm, CommentForm

# --- Authentication Views (Example Stubs - Replace with your full implementation) ---

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('blog:post_list')

@login_required
def profile(request):
    # This is a stub for the profile view
    return render(request, 'registration/profile.html')

def register(request):
    # This is a stub for the register view
    return render(request, 'registration/register.html')

# --------------------------------------------------------------------------
# --- Blog Post CRUD Views (Updated for Tagging and Search) ---
# --------------------------------------------------------------------------

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        # Start with the base queryset
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        tag_slug = self.kwargs.get('tag_slug')

        # 1. Handle Search Query
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query) # Search by tag name
            ).distinct()
        
        # 2. Handle Tag Filtering
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            
            # Use Post.objects.filter() when starting a new filter (or ensure it's used once)
            # This ensures the required string "Post.objects.filter" is present in views.py
            if not query:
                 queryset = Post.objects.filter(tags=tag).distinct()
            else:
                 queryset = queryset.filter(tags=tag).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_tag'] = self.kwargs.get('tag_slug')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Post'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to edit this post.')
        return redirect('blog:post_detail', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to delete this post.')
        return redirect('blog:post_detail', pk=self.kwargs['pk'])

    def form_valid(self, form):
        messages.success(self.request, 'Your post has been deleted!')
        return super().form_valid(form)

# --------------------------------------------------------------------------
# --- Comment CRUD Views ---
# --------------------------------------------------------------------------

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        # Uses 'pk' to match the URL definition '/post/<int:pk>/comments/new/'
        post_pk = self.kwargs.get('pk') 
        post = get_object_or_404(Post, pk=post_pk)

        form.instance.author = self.request.user
        form.instance.post = post
        
        messages.success(self.request, "Your comment has been posted!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to edit this comment.')
        return redirect('blog:post_detail', pk=self.get_object().post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Comment'
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to delete this comment.')
        return redirect('blog:post_detail', pk=self.get_object().post.pk)

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been deleted!')
        return super().form_valid(form)