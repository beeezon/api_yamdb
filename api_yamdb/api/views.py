
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from reviews.models import Users, Categories, Genres, Titles, Reviews
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsAuthorAdminModerOrReadOnly
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
            return Response(
                'Невозможно получить Token',
                status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = get_object_or_404(
                Users, username=serializer.data.get('username'))
            token_code = default_token_generator.make_token(user)
            send_mail(
                'код активации',
                f'Вы получили код авторизации {token_code}',
                'admin@django.com',
                [serializer.data.get('email')],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetWorkingTokenAPIView(TokenObtainPairView):
    """Генерация основного ключа token с проверкой кода из письма."""
    def post(self, request):
        serializers = JwsTokenSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = get_object_or_404(
                Users,
                username=request.data.get('username'))
            confirmation_code = serializers.validated_data.get(
                'confirmation_code')
            if default_token_generator.check_token(user, confirmation_code):
                token = RefreshToken.for_user(user)
                response = {}
                response['access_token'] = str(token.access_token)
                return Response(response)
            return Response(
                'Невозможно получить Token',
                status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, IsAuthorAdminModerOrReadOnly,)
    search_fields = ('username',)


    @action(detail=False, url_path='me', methods=['get', 'patch'],) #permission_classes=[IsAuthenticated, IsAuthorAdminModerOrReadOnly]
    def only_user(self, request):
        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                role = request.user.role
                assignable_role = serializer.validated_data.get('role')
                if (role == 'user'
                    and assignable_role == ('admin'
                                            or 'moderator'
                                            or None)):
                    return Response(
                        serializer.data,
                        status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UsersSerializer(request.user)
        return Response(serializer.data)
            

class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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
