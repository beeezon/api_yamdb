from reviews.models import User, Reviews, Comments
from rest_framework import serializers
from reviews.models import Reviews,Comments


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
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