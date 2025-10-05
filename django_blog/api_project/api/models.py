from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"