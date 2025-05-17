# copy all tests from test_position.py but adapt them to test_status.py

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from employee.models.status import Status, StatusChoices

User = get_user_model()


class StatusCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("status-list")

    def test_should_return_success_when_creating_status(self):
        data = {
            "name": StatusChoices.CONTRACT,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_should_return_error_when_creating_status_with_invalid_data(self):
        data = {
            "name": "invalid",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(
            response.data["name"][0],
            '"invalid" is not a valid choice.',
        )

    def test_should_return_error_when_creating_status_without_authentication(self):
        self.client.credentials()
        data = {
            "name": StatusChoices.RETIRED,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)


class StatusListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("status-list")

    def test_should_return_list_of_statuses(self):
        Status.objects.all().delete()
        Status.objects.create(name=StatusChoices.RETIRED)
        Status.objects.create(name=StatusChoices.CONTRACT)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("id", response.data[0])
        self.assertIn("name", response.data[0])
        self.assertIn("id", response.data[1])
        self.assertIn("name", response.data[1])

    def test_should_return_error_when_listing_statuses_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)


class StatusUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="test@example.com", password=cls.password
        )
        cls.status = Status.objects.create(
            name=StatusChoices.RETIRED,
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("status-detail", args=[self.status.id])

    def test_should_return_success_when_updating_status(self):
        payload = {
            "name": StatusChoices.CONTRACT,
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], payload["name"])

    def test_should_return_error_when_updating_status_with_invalid_data(self):
        payload = {
            "name": "invalid",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(
            response.data["name"][0],
            '"invalid" is not a valid choice.',
        )

    def test_should_return_error_when_updating_status_with_invalid_id(self):
        invalid_url = reverse("status-detail", args=[999])
        payload = {
            "name": StatusChoices.CONTRACT,
        }
        response = self.client.patch(invalid_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_updating_status_without_authentication(self):
        self.client.credentials()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StatusRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="test@example.com", password=cls.password
        )
        cls.status = Status.objects.create(
            name=StatusChoices.RETIRED,
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("status-detail", args=[self.status.id])

    def test_should_return_status_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], self.status.name)

    def test_should_return_error_when_retrieving_with_invalid_id(self):
        invalid_url = reverse("status-detail", args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_retrieving_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StatusDeleteTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="test@example.com", password=cls.password
        )
        cls.status = Status.objects.create(
            name=StatusChoices.RETIRED,
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("status-detail", args=[self.status.id])

    def test_should_return_success_when_deleting_status(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Status.objects.filter(id=self.status.id, deleted_at__isnull=True).count(), 0
        )

    def test_should_return_error_when_deleting_status_with_invalid_id(self):
        invalid_url = reverse("status-detail", args=[999])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_deleting_status_without_authentication(self):
        self.client.credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
