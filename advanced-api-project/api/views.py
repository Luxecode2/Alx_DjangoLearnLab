# api/views.py
from rest_framework import generics, permissions, filters
from django_filters import rest_framework as django_filters  # ✅ add this
from .models import Book
from .serializers import BookSerializer


# ----------------------
# LIST & DETAIL VIEWS
# ----------------------
class BookListView(generics.ListAPIView):
    """Retrieve a list of all books with filtering, searching, and ordering."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Enable filtering, searching, ordering
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields allowed for filtering
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Fields allowed for searching
    search_fields = ['title', 'author__name']

    # Fields allowed for ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """Retrieve a single book by ID."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ----------------------
# CREATE, UPDATE, DELETE
# ----------------------
class BookCreateView(generics.CreateAPIView):
    """Create a new book (authenticated users only)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """Update an existing book (authenticated users only)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """Delete a book (authenticated users only)."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
