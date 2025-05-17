from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from authentication.models import User

class RefreshTokenTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="test@email.com",
            password=cls.password,
        )

    def setUp(self):
        token = self.client.post(reverse("token_obtain_pair"), {
            "email": self.user.email,
            "password": self.password
        }).data
        self.url = reverse("token_refresh")
        self.valid_payload = {
            "refresh": token.get("refresh")
        }
        self.invalid_payload = {
            "refresh": "invalid_refresh_token"
        }

    def test_should_return_success_when_valid_refresh_token_is_provided(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_should_return_error_when_invalid_refresh_token_is_provided(self):
        response = self.client.post(self.url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)