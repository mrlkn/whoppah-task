from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to grant read-only access to all users,
    but write access to only admin users.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
