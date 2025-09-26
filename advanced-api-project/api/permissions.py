# api/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a book to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed for the owner of the book
        return obj.owner == request.user
