
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from reviews.models import User, Category, Genre, Title, Review
from rest_framework import filters, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .permissions import (UserMePermission,
                          IsAdminOrReadOnly,
                          IsAdminOrReadOnly,
                          UserPermission,
                          IsAuthorAdminModerOrReadOnly,)
from .serializers import (
    UserSerializer, ReviewSerializer, CommentSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer,
    AuthorizationTokenSerializer, JwsTokenSerializer)


class GetPostDeleteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


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


class GetWorkingTokenAPIView(TokenObtainPairView):
    """Генерация основного ключа token с проверкой кода из письма."""
    def post(self, request):
        serializers = JwsTokenSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = get_object_or_404(
                User,
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission, )
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False,
            url_path='me',
            methods=['get', 'patch'],
            permission_classes=[UserMePermission, ])
    def only_user(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
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
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.review

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)

