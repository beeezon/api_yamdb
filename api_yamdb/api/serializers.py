from email.policy import default
from django.shortcuts import get_object_or_404
from reviews.models import Users, Categories, Genres, Titles, Reviews, Comments
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


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
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=Users.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Users.objects.all())],
        required=True,
    )

    class Meta:
        fields = ('username',
                  'email',
                  'bio',
                  'last_name',
                  'first_name',
                  'role')
        model = Users
        lookup_field = 'username'

class UsersPatchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username',
                  'email',
                  'bio',
                  'last_name',
                  'first_name',
                  'role')
        model = Users
        read_only_fields = ('role',)

class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Titles, pk=title_id)
        if (Reviews.objects.filter(title=title, author=author).exists()
           and self.context.get('request').method == 'POST'):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ('id',)


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('id',)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Categories
        lookup_field = 'slug'



class SlugCategorySerializer(serializers.SlugRelatedField):
    def to_representation(self, instance):
        return CategoriesSerializer(instance).data


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        lookup_field = 'slug'
        model = Genres

class SlugGenresSerializer(serializers.SlugRelatedField):
    def to_representation(self, instance):
        return GenresSerializer(instance).data


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Titles


class RatingsTitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=False)
    genre = GenresSerializer(many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True)

    class Meta:
        model = Titles,
        fields = '__all__'
