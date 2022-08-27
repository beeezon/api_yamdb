from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "У Вас нет доступа на изменение контента!"

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated or request.user.is_superuser)


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff
