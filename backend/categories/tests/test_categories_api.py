from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from units_api.test_helper import TestHelper


class CategoryAPIViewTests(APITestCase):
    categories_url = reverse("units_api:categories:category-list-create")
    helper = TestHelper()

    def setUp(self):
        self.user = self.helper.get_user()
        self.client = self.helper.get_authenticated_client(self.user)

    def test_create_category(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["owner_id"], self.user.id)

    def test_create_category_with_duplicate_name(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }

        self.client.post(self.categories_url, data=data)
        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Category name must be unique for each user",
        )

    def test_create_category_without_name(self):
        data = {"description": "test description", "owner_id": self.user.id}

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["name"][0],
            "This field is required.",
        )

    def test_create_category_without_description(self):
        data = {
            "name": "test category",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], None)
        self.assertEqual(response.data["owner_id"], self.user.id)

    def test_create_category_without_color_hexcode(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
        }

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["owner_id"], self.user.id)
        self.assertEqual(response.data["color_hexcode"], None)

    def test_create_category_without_owner_id(self):
        data = {"name": "test category", "description": "test description"}

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["owner_id"][0],
            "This field is required.",
        )

    def test_create_category_with_owner_id_not_matching_authenticated_user(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": 999,
        }

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "owner_id field does not match authenticated user id",
        )

    def test_create_category_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
        }

        response = self.client.post(self.categories_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_get_categories(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }

        response = self.client.post(self.categories_url, data=data)
        response = self.client.get(self.categories_url)
        first_result = response.data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_result["name"], data["name"])
        self.assertEqual(first_result["description"], data["description"])
        self.assertEqual(first_result["owner_id"], self.user.id),
        self.assertEqual(first_result["color_hexcode"], data["color_hexcode"])

    def test_get_categories_with_multiple_users(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }

        response = self.client.post(self.categories_url, data=data)

        user2 = self.helper.get_user()
        client2 = self.helper.get_authenticated_client(user2)
        data["owner_id"] = user2.id
        response = client2.post(self.categories_url, data=data)

        response = self.client.get(self.categories_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["owner_id"], self.user.id)

    def test_get_categories_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_get_category_detail(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }

        response = self.client.post(self.categories_url, data=data)
        category_id = response.data["id"]
        response = self.client.get(f"{self.categories_url}{category_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["owner_id"], self.user.id),
        self.assertEqual(response.data["color_hexcode"], data["color_hexcode"])

    def test_get_category_detail_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get(f"{self.categories_url}1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_get_category_detail_with_non_existent_category(self):
        response = self.client.get(f"{self.categories_url}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_update_category(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }
        response = self.client.post(self.categories_url, data=data)
        category_id = response.data["id"]
        data["name"] = "updated category"
        response = self.client.put(f"{self.categories_url}{category_id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["owner_id"], self.user.id),
        self.assertEqual(response.data["color_hexcode"], data["color_hexcode"])

    def test_update_category_with_non_existent_category(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
            "color_hexcode": "#000000",
        }
        response = self.client.put(f"{self.categories_url}999/", data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_update_category_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.put(f"{self.categories_url}1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_update_category_with_owner_id_not_matching_authenticated_user(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": 999,
        }
        response = self.client.put(f"{self.categories_url}1/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "owner_id field does not match authenticated user id",
        )

    def test_delete_category(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": self.user.id,
        }
        response = self.client.post(self.categories_url, data=data)
        category_id = response.data["id"]
        response = self.client.delete(f"{self.categories_url}{category_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_with_non_existent_category(self):
        response = self.client.delete(f"{self.categories_url}999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Not found.")

    def test_delete_category_with_non_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.delete(f"{self.categories_url}1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided.",
        )

    def test_delete_category_with_owner_id_not_matching_authenticated_user(self):
        data = {
            "name": "test category",
            "description": "test description",
            "owner_id": 999,
        }
        response = self.client.delete(f"{self.categories_url}1/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            "owner_id field does not match authenticated user id",
        )
