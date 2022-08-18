from rest_framework import serializers

import datetime as dt

from reviews.models import Categories, Genres, Titles


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
