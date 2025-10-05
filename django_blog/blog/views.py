from django.shortcuts import render, redirect, get_object_or_404 # Ensure get_object_or_404 is imported
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
from django.db.models import Q # Make sure Q is imported for complex queries
from taggit.models import Tag # For filtering by tags

from .models import Post, Comment
from .forms import CustomUserCreationForm, ProfileEditForm, PostForm, CommentForm

# --- Authentication Views (unchanged) ---
# ... (CustomUserCreationForm, CustomLoginView, user_logout, profile functions) ...

# --- Blog Post CRUD Views (PostListView updated for search & tags) ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        tag_slug = self.kwargs.get('tag_slug') # Get tag slug from URL kwargs

        # 1. Handle Search Query
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query) # Search by tag name as well
            ).distinct()
        
        # 2. Handle Tag Filtering (takes precedence or works alongside search)
        if tag_slug:
            # Filter posts by the tag slug provided in the URL
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current search query back to the template
        context['search_query'] = self.request.GET.get('q', '') 
        # Pass the current tag slug to the template (useful for displaying the current filter)
        context['current_tag'] = self.kwargs.get('tag_slug') 
        return context

# ----------------------------------------------------------------------
# ... (PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, 
#      CommentUpdateView, CommentDeleteView - all other views remain as defined) ...
# ----------------------------------------------------------------------