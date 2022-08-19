from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet,  CommentsViewSet, ReviewsViewSet, CategoriesViewSet, GenresViewSet, TitlesViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/', CommentsViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/', ReviewsViewSet)
#router.register('categories', CategoriesViewSet, basename='category')
#router.register('genres', GenresViewSet, basename='genre')
#router.register('titles', TitlesViewSet, basename='title')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
