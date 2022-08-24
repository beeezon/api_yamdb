from django.shortcuts import get_object_or_404
from reviews.models import User, Reviews, Comments
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

#from .permissions import AuthorOrReadOnly
from .serializers import UsersSerializer, ReviewsSerializer, CommentsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        reviews= get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        return reviews.comments
        
    def perform_create(self, serializer):
        reviews = get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, reviews=reviews)