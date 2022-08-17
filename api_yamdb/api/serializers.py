from reviews.models import User
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User