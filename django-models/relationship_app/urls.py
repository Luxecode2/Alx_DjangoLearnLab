from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # -------------------------------
    # Authentication URLs
    # -------------------------------
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # -------------------------------
    # Book Views
    # -------------------------------
    path('books/', views.list_books, name='list_books'),

    # Library Detail View (class-based)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # -------------------------------
    # Role-Based Access Views
    # -------------------------------
    path('admin_view/', views.admin_view, name='admin_view'),
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    path('member_view/', views.member_view, name='member_view'),

    # -------------------------------
    # Book Management with Permissions
    # -------------------------------
    path('book/add/', views.add_book, name='add_book'),
    path('book/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
