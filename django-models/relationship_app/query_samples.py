from .models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def books_by_author(author_name):
    """
    Returns all books written by the author with the given name.
    """
    return Book.objects.filter(author__name=author_name)

# 2️⃣ List all books in a library
def books_in_library(library_name):
    """
    Returns all books in the library with the given name.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []

# 3️⃣ Retrieve the librarian for a library
def librarian_for_library(library_name):
    """
    Returns the librarian assigned to the library with the given name.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except Library.DoesNotExist:
        return None
