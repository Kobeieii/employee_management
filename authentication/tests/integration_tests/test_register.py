from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class RegisterViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("register-list")
        self.valid_payload = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "address": "123 Test St",
            "password": "testpassword",
        }

    def test_should_return_success_when_valid_data_is_provided(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertIn("employee", response.data)
        self.assertEqual(response.data["email"], self.valid_payload["email"])
        self.assertEqual(response.data["employee"]["first_name"], self.valid_payload["first_name"])
        self.assertEqual(response.data["employee"]["last_name"], self.valid_payload["last_name"])

    def test_should_return_error_when_invalid_email_is_provided(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "invalid-email"
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")

    def test_should_return_error_when_password_is_missing(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["password"] = ""
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"][0], "This field may not be blank.")

    def test_should_return_error_when_first_name_is_missing(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["first_name"] = ""
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(response.data["first_name"][0], "This field may not be blank.")

    def test_should_return_error_when_last_name_is_missing(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["last_name"] = ""
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(response.data["last_name"][0], "This field may not be blank.")

    def test_should_return_error_when_address_is_missing(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["address"] = ""
        response = self.client.post(self.url, data=invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("address", response.data)
        self.assertEqual(response.data["address"][0], "This field may not be blank.")