from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # columns in list view
    list_filter = ("publication_year", "author")           # filters on the right
    search_fields = ("title", "author")                    # search bar

# Register your models here.
