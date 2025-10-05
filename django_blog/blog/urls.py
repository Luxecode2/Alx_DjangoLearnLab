from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, user_logout # Import your custom views

app_name = 'blog'

urlpatterns = [
    # Existing blog post URLs (example)
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='user_logout'), # Using your custom logout view
    path('profile/', views.profile, name='profile'),

    # Django's built-in password change views
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('blog:password_change_done')
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),

    # You might want to add password reset views later
    # path('password_reset/', auth_views.PasswordResetView.as_view(...), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(...), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(...), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(...), name='password_reset_complete'),
]