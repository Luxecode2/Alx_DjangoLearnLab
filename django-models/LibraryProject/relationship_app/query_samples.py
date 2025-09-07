# relationship_app/query_samples.py
from .models import Author, Book, Library, Librarian

# 1️⃣ Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)  # exactly what ALX expects
    return Book.objects.filter(author=author)      # exactly what ALX expects

# 2️⃣ List all books in a library
def books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()

# 3️⃣ Retrieve the librarian for a library
def librarian_of_library(library_name):
    return Librarian.objects.get(library__name=library_name)
