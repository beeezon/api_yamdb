from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
