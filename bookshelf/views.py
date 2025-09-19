from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    return render(request, "bookshelf/create_book.html")

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookshelf/edit_book.html", {"book": book})

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookshelf/delete_book.html", {"book": book})
