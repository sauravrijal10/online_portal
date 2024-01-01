# branch/permissions.py
from rest_framework import permissions

class IsSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow superusers to create, update, or delete branches,
    but allow read-only access for other users.
    """

    def has_permission(self, request, view):
        # Allow read-only access for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow superusers to create, update, or delete branches
        return request.user and request.user.is_superuser
