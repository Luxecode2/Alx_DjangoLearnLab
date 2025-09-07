# Retrieve Books

```python
from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()
print(books)

# Retrieve a single book by ID
book = Book.objects.get(id=1)
print(book)

# Filter books by author
author_books = Book.objects.filter(author="Chinua Achebe")
print(author_books)
```
