from rest_framework import filters, viewsets

from api.permissions import IsAdminOrReadOnly
from api.serializers import CategoriesSerializer
from reviews.models import Categories


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
