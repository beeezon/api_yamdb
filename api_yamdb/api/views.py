from http import server
from reviews.models import User, Reviews, Comment, Categories, Genres, Titles
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UsersTokenSerializer, UsersSerializer, ReviewsSerializer, CommentsSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer
#send_mail



class UserAPIView(APIView):
    """"Отправка кода подтверждения."""
    def post(self, request):
        serializer = UsersTokenSerializer(data=request.data)
        return Response(serializer.data)


class UsersViewSet(viewsets.ModelViewSet): #Через джинерики с изменением pk на username
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    quesryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
