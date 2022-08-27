from rest_framework import status, permissions, filters
from django.shortcuts import get_object_or_404
from reviews.models import User, Reviews, Comments, Categories, Genres, Titles
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .permissions import IsAdminOrReadOnly, IsAuthenticated, IsAdminOrReadOnly, IsStaff
from .serializers import (
    UsersSerializer, ReviewsSerializer, CommentsSerializer,
    CategoriesSerializer, GenresSerializer, TitlesSerializer,
    AuthorizationTokenSerializer, JwsTokenSerializer)


class GetUserAPIView(APIView):
    """"Отправка кода подтверждения на указанную электронную почту."""
    def post(self, request):
        serializer = AuthorizationTokenSerializer(data=request.data)
        if serializer.initial_data.get('username') == 'me':
            return Response('Невозможно получить Token', status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = get_object_or_404(
                User, username=serializer.data.get('username'))
            token_code = default_token_generator.make_token(user)
            send_mail(
                'код активации',
                f'Вы получили код авторизации {token_code}',
                'admin@django.com',
                [serializer.data.get('email')],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            #return Response("Письмо успешно отправлено")


class GetWorkingTokenAPIView(TokenObtainPairView):
    """Генерация основного ключа token с проверкой кода из письма."""
    def post(self, request):
        serializers = JwsTokenSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=request.data.get('username'))
            confirmation_code = serializers.validated_data.get(
                'confirmation_code'
                )
            if default_token_generator.check_token(user, confirmation_code):
                token = RefreshToken.for_user(user)
                response = {}
                response['access_token'] = str(token.access_token)
                return Response(response)
            return Response('Невозможно получить Token', status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet): #Через джинерики с изменением pk на username
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsStaff)
    #filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)

    @action(detail=False, url_path='me', methods=['get', 'patch'],) #permission_classes=[IsAuthenticated, ] 
    def only_user(self, request):
        if request.method == 'PATCH':
            serializer = UsersSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        serializer = UsersSerializer(request.user)
        return Response(serializer.data)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get_queryset(self):
        reviews= get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        return reviews.comments
        
    def perform_create(self, serializer):
        reviews = get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, reviews=reviews)


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
