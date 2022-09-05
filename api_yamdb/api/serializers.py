from django.shortcuts import get_object_or_404
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
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ('title_id',)

    def validate(self, data):
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context.get('request').user
        title = get_object_or_404(Titles, id=title_id)
        if (title.reviews.filter(author=author).exists()
           and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Можно оставлять только один отзыв!'
            )
        return data

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Рейтинг может быть от 1 до 10.')
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review_id',)


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
    category = SlugCategorySerializer(
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=False
    )
    genre = SlugGenresSerializer(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Titles
