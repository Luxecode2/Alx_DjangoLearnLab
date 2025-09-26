# api/filters.py
import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
    Custom filter set for the Book model.
    Allows filtering by title (case-insensitive contains),
    publication_year (exact match), and author name (case-insensitive contains).
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    publication_year = django_filters.NumberFilter(lookup_expr='exact')
    # Filter by author name, linking through the 'author' ForeignKey
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author', 'author_name']