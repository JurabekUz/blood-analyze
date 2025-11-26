
from rest_framework import permissions
from users.models import User


class RolePermission(permissions.BasePermission):
    allowed_roles = ()
    allow_safe = False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if self.allow_safe and request.method in permissions.SAFE_METHODS:
            return True

        return user.role in self.allowed_roles


class IsAdmin(RolePermission):
    allowed_roles = (User.ADMIN,)
    allow_safe = False


class IsAdminOrReadOnly(RolePermission):
    allowed_roles = (User.ADMIN,)
    allow_safe = True


class IsDoctor(RolePermission):
    allowed_roles = (User.DOCTOR,)
