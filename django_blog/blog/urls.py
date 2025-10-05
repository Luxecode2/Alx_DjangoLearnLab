from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView,
    user_logout,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView, # Crucial addition for comment creation
    CommentUpdateView,
    CommentDeleteView,
    # Assumed these are implemented elsewhere in views.py:
    # register,
    # profile,
)

app_name = 'blog'

urlpatterns = [
    # Blog Post URLs
    path('', PostListView.as_view(), name='post_list'),
    
    # Tag URLs
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'), # Included Tag URL

    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'), # Changed name to 'post_create' for consistency
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # --- Comment URLs ---
    # 1. URL for creating a comment (requires post_pk)
    path('post/<int:post_pk>/comment/new/', CommentCreateView.as_view(), name='comment_create'),
    
    # 2. URL for editing a comment (requires comment pk)
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_edit'),
    
    # 3. URL for deleting a comment (requires comment pk)
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('blog:password_change_done')
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
]