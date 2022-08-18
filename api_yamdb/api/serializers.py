from reviews.models import User, Reviews, Comment
from rest_framework import serializers
from reviews.models import Reviews,Comment


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