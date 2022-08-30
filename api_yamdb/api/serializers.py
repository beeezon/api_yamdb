import datetime as dt

from reviews.models import Users, Categories, Genres, Titles
from rest_framework import serializers
from reviews.models import Reviews, Comments


class JwsTokenSerializer(serializers.Serializer):
    """Получение основнова токена для работы с сервисом."""

    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=512)


class AuthorizationTokenSerializer(serializers.ModelSerializer):
    """Генерация и получение токена,
    отправляемого в письме пользователю при регистрации."""

    class Meta:
        fields = ('email', 'username')
        model = Users


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'bio',
                  'last_name',
                  'first_name',
                  'role')
        model = Users
        lookup_field = 'username'


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Categories
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genres.objects.all()
    )

    class Meta:
        fields = '__all__'
        lookup_field = 'category'
        model = Titles
