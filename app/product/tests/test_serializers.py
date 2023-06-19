from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from product import choices


class ProductSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category = Category.objects.create(
            title='Product Category',
            created_by=self.user
        )

        self.product = Product.objects.create(
            title='Test Product',
            category=self.category,
            state=choices.DRAFT,
            created_by=self.user,
            price=1.25
        )

    def test_product_serializer_fields(self):
        """
        Test that the serialized product contains the expected fields.
        """

        serializer = ProductSerializer(instance=self.product)

        expected_fields = {
            'uuid', 'title', 'slug', 'price', 'category', 'state', 'created_at', 'updated_at', 'created_by', 'last_updated_by'
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)


class CategorySerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.category = Category.objects.create(
            title='Test Category',
            created_by=self.user
        )

    def test_category_serializer_fields(self):
        """
        Test that the serialized category contains the expected fields.
        """

        serializer = CategorySerializer(instance=self.category)

        self.assertEqual(set(
            serializer.data.keys()
        ), {
            'uuid', 'title', 'slug', 'created_at', 'updated_at', 'created_by', 'last_updated_by'
        })

