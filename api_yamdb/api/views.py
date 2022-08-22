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
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AuthorizationTokenSerializer, UsersSerializer, ReviewsSerializer, CommentsSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer


class GetUserAPIView(APIView):
    """"Отправка кода подтверждения на указанную электронную почту."""
    def post(self, request):
        serializer = AuthorizationTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User, username=serializer.data.get('username'))
            token_code = default_token_generator.make_token(user)
            send_mail(
                'код активации',
                f'Вы получили код авторизации {token_code}',
                'from@example.com',
                [serializer.data.get('email')],
                fail_silently=False,
            )
            return Response("Письмо успешно отправлено")
        else:
            return Response("""Валидация не прошла,
            возможно такой пользователь уже существует""")


class GetWorkingTokenAPIView(TokenObtainPairView):
    """Генерация оснокного ключа token с проверкой кода из письма."""
    def post(self, request):
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            response = {}
            response['access_token'] = str(token.access_token)
            return Response(response)
        return Response('токен не получишь')


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
