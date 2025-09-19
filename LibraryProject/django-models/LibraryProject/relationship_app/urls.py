from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    add_book_view,
    edit_book_view,
    delete_book_view,
    list_books,
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
    register_view
)

urlpatterns = [
    # Book CRUD views
    path('add_book/', add_book_view, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book_view, name='edit_book'),
    path('delete_book/<int:book_id>/', delete_book_view, name='delete_book'),
    path('books/', list_books, name='list_books'),

    # Library detail view (class-based)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Role-based views
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),

    # Authentication views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register_view, name='register'),
]
