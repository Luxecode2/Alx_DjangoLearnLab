# relationship_app/query_samples.py
from .models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
    """
    Returns a queryset of all books written by the given author.
    """
    return Book.objects.filter(author__name=author_name)


# List all books in a specific library
def books_in_library(library_name):
    """
    Returns a queryset of all books available in the specified library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []


# Retrieve the librarian for a specific library
def librarian_of_library(library_name):
    """
    Returns the Librarian object assigned to the given library.
    """
    try:
        return Librarian.objects.get.library__name(library_name)
    except Librarian.DoesNotExist:
        return None
