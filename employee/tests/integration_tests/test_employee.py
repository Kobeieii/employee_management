from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from employee.models.employee import Employee
from employee.models.status import Status

User = get_user_model()


class EmployeeCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        employee = Employee.objects.create(
            first_name="John", last_name="Doe", address="123 Main St", is_manager=True
        )
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password, employee=employee
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("employee-list")

    def test_should_return_success_when_creaeting_employee(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "address": "456 Elm St",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["first_name"], payload["first_name"])
        self.assertEqual(response.data["last_name"], payload["last_name"])
        self.assertEqual(response.data["address"], payload["address"])
        self.assertEqual(response.data["is_manager"], False)
        self.assertEqual(response.data["status"]["id"], Status.get_default_status())

    def test_should_return_error_when_creating_employee_with_invalid_data(self):
        payload = {
            "first_name": "",
            "last_name": "",
            "address": "",
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(response.data["first_name"][0], "This field may not be blank.")
        self.assertIn("last_name", response.data)
        self.assertEqual(response.data["last_name"][0], "This field may not be blank.")
        self.assertIn("address", response.data)
        self.assertEqual(response.data["address"][0], "This field may not be blank.")

    def test_should_return_error_when_creating_employee_with_invalid_status(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "address": "456 Elm St",
            "status_id": 9999,  # Assuming this status ID does not exist
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status_id", response.data)
        self.assertEqual(
            response.data["status_id"][0], 'Invalid pk "9999" - object does not exist.'
        )

    def test_should_return_error_when_creating_employee_without_authentication(self):
        self.client.credentials()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        employee = Employee.objects.create(
            first_name="John", last_name="Doe", address="123 Main St", is_manager=True
        )
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password, employee=employee
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("employee-list")

    def test_should_return_list_of_employees(self):
        for i in range(5):
            Employee.objects.create(
                first_name=f"Jane{i}",
                last_name=f"Doe{i}",
                address=f"456 Elm St {i}",
            )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_should_return_error_when_listing_employees_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeUpdateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        employee = Employee.objects.create(
            first_name="John", last_name="Doe", address="123 Main St", is_manager=True
        )
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password, employee=employee
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("employee-detail", args=[self.user.employee.id])

    def test_should_return_success_when_updating_employee(self):
        payload = {
            "first_name": "Jane",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["first_name"], payload["first_name"])

    def test_should_return_error_when_updating_employee_with_invalid_data(self):
        payload = {
            "first_name": "",
        }
        response = self.client.patch(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(response.data["first_name"][0], "This field may not be blank.")

    def test_should_return_error_when_updating_employee_without_authentication(self):
        self.client.credentials()
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        employee = Employee.objects.create(
            first_name="John", last_name="Doe", address="123 Main St", is_manager=True
        )
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password, employee=employee
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("employee-detail", args=[self.user.employee.id])

    def test_should_return_employee_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["first_name"], self.user.employee.first_name)
        self.assertEqual(response.data["last_name"], self.user.employee.last_name)
        self.assertEqual(response.data["address"], self.user.employee.address)
        self.assertEqual(response.data["is_manager"], self.user.employee.is_manager)

    def test_should_return_error_when_retrieving_employee_with_invalid_id(self):
        invalid_url = reverse("employee-detail", args=[9999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_retrieving_employee_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EmployeeDeleteTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "testpassword"
        employee = Employee.objects.create(
            first_name="John", last_name="Doe", address="123 Main St", is_manager=True
        )
        cls.user = User.objects.create_user(
            email="testuser@example.com", password=cls.password, employee=employee
        )

    def setUp(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": self.user.email, "password": self.password}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.url = reverse("employee-detail", args=[self.user.employee.id])

    def test_should_return_success_when_deleting_employee(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Employee.objects.filter(
                id=self.user.employee.id, deleted_at__isnull=True
            ).exists()
        )

    def test_should_return_error_when_deleting_employee_with_invalid_id(self):
        invalid_url = reverse("employee-detail", args=[9999])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_error_when_deleting_employee_without_authentication(self):
        self.client.credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
