# api/views.py (updated)
from rest_framework import generics, permissions, filters # Import filters
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .filters import BookFilter # Import BookFilter

# Views for the Book model
class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all books or create a new book.
    - GET /books/: Returns a list of all books. Supports filtering, searching, and ordering.
      Example: /books/?publication_year=1949&search=1984&ordering=-publication_year
    - POST /books/: Creates a new book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # --- Filtering, Searching, Ordering ---
    filter_backends = [
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend, # Use the backend for django-filter
        filters.OrderingFilter
    ]
    # Define fields for searching
    search_fields = ['title', 'author__name']
    # Define fields for filtering using the custom BookFilter
    filterset_class = BookFilter
    # Define fields for ordering
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title'] # Default ordering

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific book by ID.
    - GET /books/<int:pk>/: Returns details of a specific book.
    - PUT /books/<int:pk>/: Updates an existing book. Requires authentication.
    - PATCH /books/<int:pk>/: Partially updates an existing book. Requires authentication.
    - DELETE /books/<int:pk>/: Deletes a book. Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ... Author views remain the same ...
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]