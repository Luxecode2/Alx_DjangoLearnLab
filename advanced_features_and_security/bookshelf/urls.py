from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # For login/logout

urlpatterns = [
    # Task 1 - Custom User login example (if you set up custom login forms)
    # path('login/', auth_views.LoginView.as_view(template_name='bookshelf/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Task 2 - Book management views with permission checks
    path('books/', views.book_list, name='book_list'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]