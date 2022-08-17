from django.shortcuts import get_object_or_404
from reviews.models import User
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

#from .permissions import AuthorOrReadOnly
from .serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer