# api/views.py
from rest_framework import generics, permissions, filters as drf_filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters  # ✅ filtering support
from .models import Book
from .serializers import BookSerializer
from .permissions import IsOwnerOrReadOnly


# LIST VIEW (anyone can read, but only published books)
class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.DjangoFilterBackend,   # ✅ filtering
        drf_filters.SearchFilter,      # ✅ searching
        drf_filters.OrderingFilter     # ✅ ordering
    ]
    filterset_fields = ["title", "publication_year", "author"]  # filtering
    search_fields = ["title", "author__name"]  # searching
    ordering_fields = ["title", "publication_year"]  # ordering

    def get_queryset(self):
        """
        Only return published books.
        """
        return Book.objects.filter(is_published=True)


# DETAIL VIEW (anyone can read)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CREATE VIEW (only authenticated users can create)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthenticated]  # both styles

    def perform_create(self, serializer):
        """
        Attach the logged-in user as the owner of the book.
        """
        serializer.save(owner=self.request.user)


# UPDATE VIEW (only owner can update)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """
        Ensure additional validation logic can go here.
        """
        serializer.save()


# DELETE VIEW (only owner can delete)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthenticated, IsOwnerOrReadOnly]
