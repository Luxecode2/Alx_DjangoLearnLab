from django.db import models


class Author(models.Model):
    """
    Author model represents a book writer.
    One author can have multiple books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model representing a single book.
    Now includes an 'owner' field linking to the user who created it.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        'Author',
        related_name='books',
        on_delete=models.CASCADE
    )
    # NEW: Link the book to the user who created it (the owner)
    owner = models.ForeignKey(
        User,
        related_name='books_owned',
        on_delete=models.CASCADE,
        null=True # Allow null temporarily if running makemigrations on existing data
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
