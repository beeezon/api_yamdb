from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (UsersViewSet, CommentsViewSet, ReviewsViewSet,
                    CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    GetWorkingTokenAPIView, GetUserAPIView)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoriesViewSet, basename='category')
router_v1.register('genres', GenresViewSet, basename='genre')
router_v1.register('titles', TitlesViewSet, basename='title')
router_v1.register('users', UsersViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', GetUserAPIView.as_view()),
    path('v1/auth/token/', GetWorkingTokenAPIView.as_view()),
]
