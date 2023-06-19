from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from . import choices
from .custom_pagination import ProductPagination
from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer, ProductStateUpdateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "uuid"


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(state=choices.ACCEPTED)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    pagination_class = ProductPagination

    def update_product_state(self, request: Request, *args, **kwargs) -> Response:
        instance = Product.objects.filter(uuid=self.kwargs.get("pk")).first()
        if not instance:
            return Response("Product not found with the given uuid.", status=status.HTTP_404_NOT_FOUND)
        serializer = ProductStateUpdateSerializer(
            instance,
            data=request.data,
            context={"user": self.request.user}
        )
        serializer.is_valid(raise_exception=True)

        updated_instance = serializer.update(instance, serializer.validated_data)
        if not updated_instance:
            return Response({"message", "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Product state updated successfully."}, status=status.HTTP_200_OK)
