from rest_framework import serializers

from reviews.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        lookup_field = 'id'
        model = Categories
