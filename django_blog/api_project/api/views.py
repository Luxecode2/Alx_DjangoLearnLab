from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    A simple view to list all books. This is a basic example
    before moving to ViewSets.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    This provides all CRUD operations automatically.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Permission setup:
    # - IsAdminUser for 'create', 'update', 'partial_update', and 'destroy'
    # - AllowAny for 'list' and 'retrieve' (read-only access)
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]