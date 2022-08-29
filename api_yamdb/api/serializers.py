import datetime as dt
from django.shortcuts import get_object_or_404

from reviews.models import User, Category, Genre, Title
from rest_framework import exceptions, serializers
from reviews.models import Review, Comment


class JwsTokenSerializer(serializers.Serializer):
    """Получение основнова токена для работы с сервисом."""

    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=512)


class AuthorizationTokenSerializer(serializers.ModelSerializer):
    """Генерация и получение токена,
    отправляемого в письме пользователю при регистрации."""

    class Meta:
        fields = ('email', 'username')
        model = User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'bio',
                  'last_name',
                  'first_name',
                  'role')
        model = User
        lookup_field = 'username'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST'
           and Review.objects.filter(title=title, author=author).exists()):
            raise exceptions.ValidationError(
                'Нельзя добавить больше одного отзыва к произведению!')
        return data

    class Meta:
        fields = '__all__'
        read_only_field = ('id',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review_id',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('id',)
        lookup_field = 'category'
        model = Title

    def validate(self, data):
        if dt.datetime().year < data.year:
            raise serializers.ValidationError(
                '''
                Путешествия в будущее запрещены!
                Год создения произведения не может быть позже текущего!
                '''
            )
        return data

