import datetime as dt

from reviews.models import User, Reviews, Comment, Categories, Genres, Titles
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class ReceivingMainTokenSerializer(TokenObtainSerializer):
    """Получение основнова токена для работы с сервисом."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        del self.fields['password']
        self.fields['confirmation_code'] = serializers.CharField()


class AuthorizationTokenSerializer(serializers.ModelSerializer):
    """Генерация и получение токена,
    отправляемого в письме пользователю при регистрации."""

    class Meta:
        fields = ('email', 'username')
        model = User


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = 'slug'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Categories.objects.all()
    )

    class Meta:
        fileds = '__all__'
        lookup_field = 'category'
        model = Titles

    def validate(self, data):
        if dt.datetime().year < data.year:
            raise serializers.ValidationError(
                '''
                Путешествия в будущее запрещены!
                Год создения произведения не может быть позже текущего!
                '''
            )
        return data
