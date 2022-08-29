from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, CommentViewSet, ReviewViewSet,
                    CategoryViewSet, GenreViewSet, TitleViewSet,
                    GetWorkingTokenAPIView, GetUserAPIView, )

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register(r'users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', GetUserAPIView.as_view()),
    path('v1/auth/token/', GetWorkingTokenAPIView.as_view()),
]
