from django.test import TestCase
from authentication.serializers import RegisterSerializer

class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "email": "test@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "image": None,
            "password": "password123",
        }
        self.invalid_data = {
            "email": "invalid-email",
            "first_name": "",
            "last_name": "",
            "address": "",
            "image": None,
            "password": "",
        }
        self.serializer = RegisterSerializer(data=self.valid_data)
        self.serializer_invalid = RegisterSerializer(data=self.invalid_data)

    def test_should_return_success_when_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())
        self.assertEqual(
            self.serializer.validated_data["email"], self.valid_data["email"]
        )
        self.assertEqual(
            self.serializer.validated_data["first_name"], self.valid_data["first_name"]
        )
        self.assertEqual(
            self.serializer.validated_data["last_name"], self.valid_data["last_name"]
        )
        self.assertEqual(
            self.serializer.validated_data["address"], self.valid_data["address"]
        )
        self.assertEqual(
            self.serializer.validated_data["image"], self.valid_data["image"]
        )
        self.assertEqual(
            self.serializer.validated_data["password"], self.valid_data["password"]
        )

    def test_should_return_err_when_invalid_serializer(self):
        self.assertFalse(self.serializer_invalid.is_valid())
        self.assertIn("email", self.serializer_invalid.errors)
        self.assertIn("first_name", self.serializer_invalid.errors)
        self.assertIn("last_name", self.serializer_invalid.errors)
        self.assertIn("address", self.serializer_invalid.errors)
        self.assertIn("password", self.serializer_invalid.errors)
        self.assertEqual(
            self.serializer_invalid.errors["email"], ["Enter a valid email address."]
        )
        self.assertEqual(
            self.serializer_invalid.errors["first_name"], ["This field may not be blank."]
        )
        self.assertEqual(
            self.serializer_invalid.errors["last_name"], ["This field may not be blank."]
        )
        self.assertEqual(
            self.serializer_invalid.errors["address"], ["This field may not be blank."]
        )
        self.assertEqual(
            self.serializer_invalid.errors["password"], ["This field may not be blank."]
        )