from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from employee.models.position import Position

User = get_user_model()


class PositionCreateTestCase(APITestCase):
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
        self.url = reverse("position-list")

    def test_should_return_success_when_creating_position(self):
        data = {
            "name": "Software Engineer",
            "salary": 65000,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["salary"], data["salary"])

    def test_should_return_error_when_creating_position_with_invalid_data(self):
        data = {
            "name": "",
            "salary": "as",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("salary", response.data)
        self.assertEqual(response.data["name"][0], "This field may not be blank.")
        self.assertEqual(response.data["salary"][0], "A valid number is required.")

    def test_should_return_error_when_creating_position_with_existing_name(self):
        Position.objects.create(name="Software Engineer", salary=65000)
        data = {
            "name": "Software Engineer",
            "salary": 70000,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(
            response.data["name"][0], "position with this name already exists."
        )

    def test_should_return_error_when_creating_position_without_authentication(self):
        self.client.credentials()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PositionListTestCase(APITestCase):
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
        self.url = reverse("position-list")

    def test_should_return_list_of_positions(self):
        for i in range(5):
            Position.objects.create(
                name=f"Software Engineer {i}",
                salary=65000 + (i * 1000),
            )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_should_return_error_when_listing_positions_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PositionUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password
        )
        cls.position = Position.objects.create(
            name="Software Engineer",
            salary=65000,
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("position-detail", args=[self.position.id])

    def test_should_return_success_when_updating_position(self):
        payload = {
            "salary": 75000,
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], self.position.name)
        self.assertEqual(response.data["salary"], payload["salary"])

    def test_should_return_error_when_updating_position_with_invalid_data(self):
        payload = {
            "name": "",
            "salary": "invalid",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(response.data["name"][0], "This field may not be blank.")
        self.assertIn("salary", response.data)
        self.assertEqual(response.data["salary"][0], "A valid number is required.")

    def test_should_return_error_when_updating_position_without_authentication(self):
        self.client.credentials()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PositionRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password
        )
        cls.position = Position.objects.create(
            name="Software Engineer",
            salary=65000,
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("position-detail", args=[self.position.id])

    def test_should_return_position_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], self.position.name)
        self.assertEqual(response.data["salary"], self.position.salary)

    def test_should_return_error_when_retrieving_with_invalid_id(self):
        invalid_url = reverse("position-detail", args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_retrieving_position_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PositionDeleteTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password
        )
        cls.position = Position.objects.create(
            name="Software Engineer",
            salary=65000,
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("position-detail", args=[self.position.id])

    def test_should_return_success_when_deleting_position(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Position.objects.filter(
                id=self.position.id, deleted_at__isnull=True
            ).count(),
            0,
        )

    def test_should_return_error_when_deleting_position_with_invalid_id(self):
        invalid_url = reverse("position-detail", args=[999])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_deleting_position_without_authentication(self):
        self.client.credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
