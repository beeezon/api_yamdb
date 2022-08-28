from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = "У Вас нет доступа на изменение контента!"

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsAuthorAdminModerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # return (request.method in permissions.SAFE_METHODS
        #         or request.user.is_authenticated)
        return (request.method == ('GET') and request.user.role == 'admin' or 
        request.method == ('PATCH') and request.user.is_authenticated)
        # return (request.method in permissions.SAFE_METHODS
        #         or request.user.is_authenticated)


class UserMePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == 'PATCH' or 'GET':
                return True
        return False


class AnonimPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        pass


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        LIMITED_METHODS = ['PUT', 'PATCH', 'DELETE']
        if request.method in LIMITED_METHODS and request.user == obj.author:
            return True
        return False
