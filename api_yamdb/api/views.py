from reviews.models import User, Reviews, Comment, Categories, Genres, Titles
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from .serializers import UsersTokenSerializer, UsersSerializer, ReviewsSerializer, CommentsSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer
#send_mail


class UserAPIView(APIView):
    """"Отправка кода подтверждения."""
    def post(self, request):
        serializer = UsersTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=serializer.data.get('username'))
            token_code = default_token_generator.make_token(user)
            send_mail(
                'код активации',
                f'Вы получили код авторизации {token_code}',
                'from@example.com',
                [serializer.data.get('email')],
                fail_silently=False,
            )
            #serializer.save(confirmation_code=token_code)
            return Response("Письмо успешно отправлено")
        else:
            return Response("Валидация не прошла")


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
