from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UnitsUser


class TestHelper:
    def __init__(self) -> None:
        self.fake = Faker()

    def get_authenticated_client(serf, user):
        access_token = RefreshToken.for_user(user).access_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        return client

    def get_user(self):
        user = UnitsUser.objects.create_user(
            email=self.fake.email(),
            username=self.fake.first_name(),
            password="testpassword",
        )

        return user
