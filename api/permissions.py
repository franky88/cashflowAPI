from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsSuperAdminOrOwner(BasePermission):
    """
    Allows full access to superusers.
    Owners can view and edit their own objects.
    Other users can only read.
    """

    def has_permission(self, request, view):
        # Allow all authenticated users (adjust if you want more strict rules)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner or a superuser
        return obj.user == request.user or request.user.is_superuser
