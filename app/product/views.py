# marketplace/views.py

from rest_framework import viewsets, permissions

from . import choices
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(state=choices.ACCEPTED)
    serializer_class = ProductSerializer
