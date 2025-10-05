from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post # Import your Post model
from .forms import CustomUserCreationForm, ProfileEditForm, PostForm # Import forms


# --- Authentication Views (from previous task - kept for context) ---

# Custom Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the blog.')
            return redirect('blog:post_list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

# Custom Logout View
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog:post_list')

# Profile Management View
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

# --- Blog Post CRUD Views ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # Name of the queryset variable in the template
    ordering = ['-created_at'] # Order posts by newest first (can also be done in model Meta)
    paginate_by = 5 # Optional: for pagination

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' # <app>/<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm # Use the custom form
    template_name = 'blog/post_form.html'
    # fields = ['title', 'content'] # If not using form_class, specify fields directly

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author to the logged-in user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Post'
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm # Use the custom form
    template_name = 'blog/post_form.html'
    # fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # Re-set author in case it's accidentally changed (good practice)
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)

    def test_func(self):
        # Ensure only the author can update the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to edit this post.')
        return redirect('blog:post_detail', pk=self.kwargs['pk']) # Redirect to detail page with error

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list') # Redirect to post list after deletion

    def test_func(self):
        # Ensure only the author can delete the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        messages.error(self.request, 'You are not authorized to delete this post.')
        return redirect('blog:post_detail', pk=self.kwargs['pk']) # Redirect to detail page with error

    def form_valid(self, form):
        messages.success(self.request, 'Your post has been deleted!')
        return super().form_valid(form)