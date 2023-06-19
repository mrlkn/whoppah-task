from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "products/<uuid:pk>/update_state/",
        ProductViewSet.as_view({"put": "update_product_state"}),
        name="update-product-state",
    ),
]
