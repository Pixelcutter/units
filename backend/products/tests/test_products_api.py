from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from units_api.test_helper import TestHelper
from categories.models import Category

# TODO: test that user owns the category that is assigned to a product


class ProductAPIViewTests(APITestCase):
    products_url = reverse("units_api:products:product-list-create")
    helper = TestHelper()

    def setUp(self):
        self.user = self.helper.get_user()
        self.client = self.helper.get_authenticated_client(self.user)

        self.category = Category.objects.create(
            name="test category", owner_id=self.user
        )
        self.category.save()

        self.data = {
            "name": "test product",
            "description": "test description",
            "category": self.category.id,
            "owner_id": self.user.id,
            "quantity": 5,
            "for_sale": True,
            "price": 10.99,
            "image_url": "https://www.google.com",
        }

    def test_create_product(self):
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["description"], self.data["description"])
        self.assertEqual(response.data["category"], self.data["category"])
        self.assertEqual(response.data["owner_id"], self.user.id)
        self.assertEqual(response.data["quantity"], self.data["quantity"])
        self.assertEqual(response.data["for_sale"], self.data["for_sale"])
        self.assertEqual(float(response.data["price"]), self.data["price"])
        self.assertEqual(response.data["image_url"], self.data["image_url"])

    def test_create_product_with_duplicate_name(self):
        self.client.post(self.products_url, data=self.data)
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Product name must be unique for each user",
        )

    def test_create_product_without_name(self):
        del self.data["name"]
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["name"][0],
            "This field is required.",
        )

    def test_create_product_without_description(self):
        del self.data["description"]
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_without_category(self):
        del self.data["category"]
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_without_owner_id(self):
        del self.data["owner_id"]
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["owner_id"][0],
            "This field is required.",
        )

    def test_create_product_with_owner_id_not_matching_authenticated_user(self):
        self.data["owner_id"] = 999
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "owner_id field does not match authenticated user id",
        )

    def test_create_product_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.post(self.products_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_get_categories(self):
        response = self.client.post(self.products_url, data=self.data)
        response = self.client.get(self.products_url)
        first_result = response.data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_result["name"], self.data["name"])
        self.assertEqual(first_result["description"], self.data["description"])
        self.assertEqual(first_result["owner_id"], self.data["owner_id"]),
        self.assertEqual(first_result["category"], self.data["category"])
        self.assertEqual(first_result["quantity"], self.data["quantity"])
        self.assertEqual(first_result["for_sale"], self.data["for_sale"])
        self.assertEqual(float(first_result["price"]), self.data["price"])
        self.assertEqual(first_result["image_url"], self.data["image_url"])

    def test_get_categories_with_multiple_users(self):
        response = self.client.post(self.products_url, data=self.data)

        user2 = self.helper.get_user()
        client2 = self.helper.get_authenticated_client(user2)
        self.data["owner_id"] = user2.id
        response = client2.post(self.products_url, data=self.data)

        response = self.client.get(self.products_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["owner_id"], self.user.id)

    def test_get_categories_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_get_product_detail(self):
        response = self.client.post(self.products_url, data=self.data)
        product_id = response.data["id"]
        response = self.client.get(f"{self.products_url}{product_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["description"], self.data["description"])
        self.assertEqual(response.data["owner_id"], self.data["owner_id"]),
        self.assertEqual(response.data["category"], self.data["category"])
        self.assertEqual(response.data["quantity"], self.data["quantity"])
        self.assertEqual(response.data["for_sale"], self.data["for_sale"])
        self.assertEqual(float(response.data["price"]), self.data["price"])
        self.assertEqual(response.data["image_url"], self.data["image_url"])

    def test_get_product_detail_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(f"{self.products_url}999/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_get_product_detail_with_non_existent_product(self):
        response = self.client.get(f"{self.products_url}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_update_product(self):
        response = self.client.post(self.products_url, data=self.data)
        product_id = response.data["id"]
        self.data["name"] = "updated product"
        response = self.client.put(f"{self.products_url}{product_id}/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.data["name"])
        self.assertEqual(response.data["description"], self.data["description"])
        self.assertEqual(response.data["owner_id"], self.data["owner_id"]),
        self.assertEqual(response.data["category"], self.data["category"])
        self.assertEqual(response.data["quantity"], self.data["quantity"])
        self.assertEqual(response.data["for_sale"], self.data["for_sale"])
        self.assertEqual(float(response.data["price"]), self.data["price"])
        self.assertEqual(response.data["image_url"], self.data["image_url"])

    def test_update_product_with_non_existent_product(self):
        response = self.client.put(f"{self.products_url}999/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_update_product_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.put(f"{self.products_url}1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_update_product_with_owner_id_not_matching_authenticated_user(self):
        self.data["owner_id"] = 999
        response = self.client.put(f"{self.products_url}1/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "owner_id field does not match authenticated user id",
        )

    def test_delete_product(self):
        response = self.client.post(self.products_url, data=self.data)
        product_id = response.data["id"]
        response = self.client.delete(f"{self.products_url}{product_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_with_non_existent_product(self):
        response = self.client.delete(f"{self.products_url}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_delete_product_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.delete(f"{self.products_url}1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_delete_product_with_owner_id_not_matching_authenticated_user(self):
        self.data["owner_id"] = 999
        response = self.client.delete(f"{self.products_url}1/", data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "owner_id field does not match authenticated user id",
        )
