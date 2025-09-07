# relationship_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Book listing
    path("books/", views.list_books, name="list_books"),
    
    # Library details
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
    
    # Role-based views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
    
    # Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
