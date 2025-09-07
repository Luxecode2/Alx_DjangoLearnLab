```python
from bookshelf.models import Book

# Retrieve all Book objects
all_books = Book.objects.all()
print(all_books)
# Output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>
```
