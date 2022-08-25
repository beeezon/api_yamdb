import datetime as dt


from reviews.models import User, Reviews, Comments, Categories, Genres, Titles
from rest_framework import serializers
from reviews.models import Reviews,Comments


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


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'bio', 'last_name', 'first_name', 'role') # тут не все поля нужны
        model = User
        



class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review_id',)


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
