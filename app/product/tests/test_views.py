from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from product import choices
from product.models import Category, Product


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.category_data = {"title": "Electronics"}
        self.category = Category.objects.create(
            title="Electronics", created_by=self.user
        )
        self.admin_user = User.objects.create_user(
            username="admin", password="admin", is_staff=True
        )

    def test_get_list_of_categories(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_category(self):
        url = reverse("category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_user_cannot_create_category(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("category-list")
        response = self.client.post(url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_user_cannot_update_category(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.put(url, {"title": "Updated Electronics"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_user_cannot_delete_category(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_create_category(self):
        self.client.login(username="admin", password="admin")
        url = reverse("category-list")
        response = self.client.post(url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_user_can_update_category(self):
        self.client.login(username="admin", password="admin")
        url = reverse("category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.put(url, {"title": "Updated Electronics"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_delete_category(self):
        self.client.login(username="admin", password="admin")
        url = reverse("category-detail", kwargs={"uuid": self.category.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.category = Category.objects.create(
            title="Electronics", created_by=self.user
        )
        self.product_data = {
            "title": "Laptop",
            "category": self.category.uuid,
            "price": 1.25,
        }
        self.admin_user = User.objects.create_user(
            username="admin", password="admin", is_staff=True
        )

    def test_authenticated_user_can_create_product(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("product-list")
        response = self.client.post(url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().title, "Laptop")

    def test_unauthenticated_user_cannot_create_product(self):
        url = reverse("product-list")
        response = self.client.post(url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 0)

    def test_only_accepted_products_are_listed(self):
        Product.objects.create(
            title="Apple pro vision xd",
            category=self.category,
            created_by=self.user,
            price=1.25,
        )

        self.client.login(username="testuser", password="testpassword")

        accepted_product = Product.objects.create(
            title="Tablet",
            category=self.category,
            created_by=self.user,
            price=1.25,
            state=choices.ACCEPTED,
        )

        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], accepted_product.title)

    def test_authorized_user_can_update_product_state(self):
        product = Product.objects.create(
            title="iphone pro x max ultra diamond gold",
            category=self.category,
            created_by=self.user,
            price=1.25,
        )

        self.client.login(username="testuser", password="testpassword")

        data = {"state": "new"}

        url = reverse("update-product-state", kwargs={"pk": product.uuid})
        response = self.client.put(url, data)

        product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product.state, "new")

    def test_unauthorized_user_cannot_update_product_state(self):
        product = Product.objects.create(
            title="Smartphone",
            category=self.category,
            price=1.25,
            created_by=self.admin_user,
        )

        self.client.login(username="testuser", password="testpassword")

        data = {"state": "accepted"}

        url = reverse("update-product-state", kwargs={"pk": product.uuid})
        response = self.client.put(url, data)

        product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(product.state, "accepted")

    def test_invalid_state_transition_is_rejected(self):
        product = Product.objects.create(
            title="Smartphone",
            category=self.category,
            price=1.25,
            created_by=self.admin_user,
        )

        self.client.login(username="admin", password="admin")

        data = {"state": "draft"}

        url = reverse("update-product-state", kwargs={"pk": product.uuid})
        response = self.client.put(url, data)

        product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(product.state, "draft")
