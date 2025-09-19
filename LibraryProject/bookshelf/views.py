from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.forms import ModelForm
from .models import Book # Assuming Book model is defined in models.py

# A simple form for demonstration purposes, matching the fields in Book model.
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']

@login_required # Ensures only logged-in users can access
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Displays a list of all books. Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Handles creating new books. Requires 'can_create' permission.
    The 'added_by' field is automatically set to the logged-in user.
    """
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.added_by = request.user # Assign the current user as the adder
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/form_example.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_update(request, pk):
    """
    Handles updating an existing book. Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'bookshelf/form_example.html', {'form': form, 'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Handles deleting a book. Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    # For GET request, display a confirmation page
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})