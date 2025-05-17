from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from employee.models.department import Department
from employee.models.employee import Employee

User = get_user_model()


class DepartmentCreateTestCase(APITestCase):
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
        self.url = reverse("department-list")

    def test_should_return_success_when_creating_department(self):
        data = {"name": "IT Department", "manager_id": self.user.employee.id}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.first().name, "IT Department")

    def test_should_return_error_when_creating_department_without_name(self):
        data = {"name": "", "manager_id": self.user.employee.id}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(response.data["name"], ["This field may not be blank."])

    def test_should_return_error_when_creating_department_with_employee(self):
        employee = Employee.objects.create(
            first_name="Jane", last_name="Smith", address="456 Elm St", is_manager=False
        )
        data = {"name": "IT Department", "manager_id": employee.id}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("manager_id", response.data)
        self.assertEqual(
            response.data["manager_id"], ["This employee is not marked as a manager."]
        )

    def test_should_return_error_when_creating_department_with_deleted_employee(self):
        employee = Employee.objects.create(
            first_name="Jane", last_name="Smith", address="456 Elm St", is_manager=True
        )
        employee.delete()

        data = {"name": "IT Department", "manager_id": employee.id}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("manager_id", response.data)
        self.assertEqual(response.data["manager_id"], ["This employee is deleted."])

    def test_should_return_error_when_creating_department_with_unauthenticated_user(
        self,
    ):
        self.client.credentials()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentListTestCase(APITestCase):
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
        self.url = reverse("department-list")

    def test_should_return_list_of_departments(self):
        for i in range(2):
            employee = Employee.objects.create(
                first_name=f"Manager {i}",
                last_name=f"Last {i}",
                address=f"Address {i}",
                is_manager=True,
            )
            Department.objects.create(
                name=f"Department {i}",
                manager=employee,
            )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_should_return_empty_list_when_no_departments_exist(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_should_return_error_when_unauthenticated_user_tries_to_access_list(self):
        self.client.credentials()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentUpdateTestCase(APITestCase):
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
        self.department = Department.objects.create(
            name="IT Department", manager=self.user.employee
        )
        self.url = reverse("department-detail", args=[self.department.id])

    def test_should_return_success_when_updating_department(self):
        data = {"name": "Updated Department"}

        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Department")

    def test_should_return_error_when_updating_department_with_invalid_name(self):
        data = {"name": ""}

        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(response.data["name"], ["This field may not be blank."])

    def test_should_return_error_when_updating_department_with_deleted_employee(self):
        employee = Employee.objects.create(
            first_name="Jane", last_name="Smith", address="456 Elm St", is_manager=True
        )
        employee.delete()

        data = {"name": "Updated Department", "manager_id": employee.id}

        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("manager_id", response.data)
        self.assertEqual(response.data["manager_id"], ["This employee is deleted."])

    def test_should_return_error_when_updating_department_with_unauthenticated_user(
        self,
    ):
        self.client.credentials()
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentRetrieveTestCase(APITestCase):
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
        self.department = Department.objects.create(
            name="IT Department", manager=self.user.employee
        )
        self.url = reverse("department-detail", args=[self.department.id])

    def test_should_return_department_details(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "IT Department")
        self.assertEqual(
            response.data["manager"]["first_name"], self.user.employee.first_name
        )
        self.assertEqual(
            response.data["manager"]["last_name"], self.user.employee.last_name
        )

    def test_should_return_error_when_department_does_not_exist(self):
        url = reverse("department-detail", args=[9999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"], "No Department matches the given query."
        )

    def test_should_return_error_when_unauthenticated_user_tries_to_access_department(
        self,
    ):
        self.client.credentials()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentDeleteTestCase(APITestCase):
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
        self.department = Department.objects.create(
            name="IT Department", manager=self.user.employee
        )
        self.url = reverse("department-detail", args=[self.department.id])

    def test_should_return_success_when_deleting_department(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.filter(deleted_at__isnull=True).count(), 0)

    def test_should_return_error_when_department_does_not_exist(self):
        url = reverse("department-detail", args=[9999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"], "No Department matches the given query."
        )

    def test_should_return_error_when_unauthenticated_user_tries_to_delete_department(
        self,
    ):
        self.client.credentials()
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
