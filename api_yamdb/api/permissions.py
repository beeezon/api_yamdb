from ast import Try
from operator import truediv
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "У Вас нет доступа на изменение контента!"

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsUserRestrictions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == ('PATCH' or 'PUT' or 'DELETE'):
            return False
        if request.user.is_authenticated:
            pass