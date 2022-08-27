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


class AnonimPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        pass


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        PETMITTED_METHODS = ['GET', 'POST']
        LIMITED_METHODS = ['PUT', 'PATCH', 'DELETE']

        if request.method in LIMITED_METHODS and request.user == obj.author:
            return True
        elif request.method in PETMITTED_METHODS:
            return True
        elif request.user.role == 'admin' or 'moderator':
            return True
        else:
            return False
