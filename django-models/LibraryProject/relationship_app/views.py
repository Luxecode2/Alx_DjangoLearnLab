from .models import Library, Book
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library  # <-- ALX expects Library to be imported
from .models import Author, Book, Library, Librarian, UserProfile
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book


# Add Book
@permission_required('relationship_app.can_add_book')
def add_book_view(request):
    if request.method == 'POST':
        # handle form submission
        pass
    return render(request, 'relationship_app/add_book.html')

# Edit Book
@permission_required('relationship_app.can_change_book')
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        # handle form submission
        pass
    return render(request, 'relationship_app/edit_book.html', {'book': book})

# Delete Book
@permission_required('relationship_app.can_delete_book')
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# -----------------------
# Function-based view
# -----------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# -----------------------
# Class-based view
# -----------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# -----------------------
# User Authentication Views
# -----------------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_books')
    return render(request, 'relationship_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# -----------------------
# Role-Based Views
# -----------------------
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
