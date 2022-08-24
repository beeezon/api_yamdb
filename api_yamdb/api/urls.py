from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet,  CommentsViewSet, ReviewsViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewSet, basename='comments')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/', ReviewsViewSet, basename='reviews')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

