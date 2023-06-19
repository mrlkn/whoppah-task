from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_auto_generate_unique_slug_on_create(self):
        """
        Test that a unique slug is automatically generated upon the creation of a new category.
        """

        category = Category.objects.create(title="Test Category", created_by=self.user)

        self.assertIsNotNone(category.slug)
        self.assertEqual(category.slug, "test-category")

        category2 = Category.objects.create(title="Test Category", created_by=self.user)

        self.assertEqual(category.created_by, self.user)

        self.assertIsNotNone(category2.slug)
        self.assertNotEqual(category.slug, category2.slug)
        self.assertTrue(category2.slug.startswith("test-category"))

    def test_auto_generate_unique_slug_on_update(self):
        """
        Test that a unique slug is automatically generated upon updating the title of an existing category.
        """

        category = Category.objects.create(title="Original Title", created_by=self.user)

        category.title = "Updated Title"
        category.save()

        self.assertIsNotNone(category.slug)
        self.assertEqual(category.slug, "updated-title")

    def test_auto_generate_unique_slug_uniqueness(self):
        """
        Test that a unique slug is automatically generated with the same title.
        """

        category = Category.objects.create(title="Unique Title", created_by=self.user)

        category_two = Category.objects.create(
            title="Unique Title", created_by=self.user
        )

        self.assertNotEqual(category.slug, category_two)
