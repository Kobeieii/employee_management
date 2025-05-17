from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from authentication.models import User

class LoginViewSetTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="test@email.com",
            password=cls.password
        )
    def setUp(self):
        self.url = reverse("token_obtain_pair")
        self.valid_payload = {
            "email": self.user.email,
            "password": self.password
        }
        self.invalid_payload = {
            "email": "invalid@email.com",
            "password": "wrongpassword"
        }

    def test_should_return_success_when_valid_credentials_are_provided(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_should_return_error_when_invalid_credentials_are_provided(self):
        response = self.client.post(self.url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "No active account found with the given credentials")