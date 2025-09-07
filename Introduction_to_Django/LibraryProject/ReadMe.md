# Introduction to Django: Bookshelf App

This project demonstrates basic Django ORM usage by creating a simple **Book** model
and performing CRUD (Create, Retrieve, Update, Delete) operations through the Django shell.

---

## 📌 Book Model

Defined in `bookshelf/models.py`:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
```
