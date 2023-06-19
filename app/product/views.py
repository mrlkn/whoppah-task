from rest_framework import viewsets

from . import choices
from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "uuid"


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(state=choices.ACCEPTED)
    serializer_class = ProductSerializer
