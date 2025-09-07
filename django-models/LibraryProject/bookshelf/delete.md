### 📄 `delete.md`

This file only contains the **delete step**:

````markdown
```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Output: (1, {'bookshelf.Book': 1})

print(Book.objects.all())
# Output: <QuerySet []>
```
````
