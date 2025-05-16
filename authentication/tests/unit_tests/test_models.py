from django.test import TestCase
from django.db import IntegrityError
from authentication.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "email": "test@email.com",
            "password": "password123",
        }
        self.invalid_email_data = {
            "email": "invalid-email",
            "password": "password123",
        }
        self.invalid_password_data = {
            "email": "test@email.com",
            "password": "",
        }

    def test_should_return_success_when_creating_user(self):
        user = User.objects.create_user(**self.valid_data)
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertTrue(user.check_password(self.valid_data["password"]))

    def test_should_return_err_when_creating_user_with_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=self.invalid_email_data["email"],
                password=self.invalid_email_data["password"],
            )

    def test_should_return_err_when_creating_user_with_invalid_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=self.invalid_password_data["email"],
                password=self.invalid_password_data["password"],
            )

    def test_should_return_err_when_creating_duplicate_user(self):
        User.objects.create_user(**self.valid_data)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.valid_data)
