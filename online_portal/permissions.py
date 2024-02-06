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

class IsAdminOrSuperuser(permissions.BasePermission):
    """
    Custom permission to allow admins or superusers to create, update, or delete branches,
    but allow read-only access for other users.
    """

    def has_permission(self, request, view):
        # Allow read-only access for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin)
        # Allow admins or superusers to create, update, or delete brancheh
        # return request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin)
