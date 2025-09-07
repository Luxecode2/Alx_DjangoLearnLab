This file only contains the **update step**:

````markdown
```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
# Output: Nineteen Eighty-Four by George Orwell (1949)
```
````
