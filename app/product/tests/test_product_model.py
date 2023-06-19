from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from product.models import Category, Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.category = Category.objects.create(
            title="Test Category", created_by=self.user
        )

    def test_create_product_with_defaults(self):
        """
        Test creating a product with minimal data to ensure defaults are set correctly
        """

        product = Product.objects.create(
            title="Test Product",
            price="9.99",
            category=self.category,
            created_by=self.user,
        )

        self.assertIsNotNone(product.uuid)

        current_time = timezone.now()
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)
        self.assertTrue(current_time - product.created_at < timedelta(seconds=5))
        self.assertTrue(current_time - product.updated_at < timedelta(seconds=5))

        self.assertEqual(product.state, "draft")

    def test_auto_generate_unique_slug_on_create(self):
        """
        Test that a unique slug is automatically generated upon the creation of a new product.
        """

        product = Product.objects.create(
            title="Test Product",
            category=self.category,
            price=100.00,
            created_by=self.user,
        )

        self.assertIsNotNone(product.slug)
        self.assertEqual(product.slug, "test-product")

        product2 = Product.objects.create(
            title="Test Product",
            category=self.category,
            price=100.00,
            created_by=self.user,
        )

        self.assertIsNotNone(product2.slug)
        self.assertNotEqual(product.slug, product2.slug)
        self.assertTrue(product2.slug.startswith("test-product"))

    def test_auto_generate_unique_slug_on_update(self):
        """
        Test that a unique slug is automatically generated upon updating the title of an existing product.
        """

        product = Product.objects.create(
            title="Original Title",
            category=self.category,
            price=100.00,
            created_by=self.user,
        )

        product.title = "Updated Title"
        product.save()

        self.assertIsNotNone(product.slug)
        self.assertEqual(product.slug, "updated-title")
