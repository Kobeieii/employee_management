from django.test import TestCase
from employee.serializers.department import DepartmentSerializer
from employee.serializers.employee import EmployeeSerializer
from employee.serializers.position import PositionSerializer
from employee.serializers.status import StatusSerializer
from employee.models.employee import Employee
from employee.models.status import StatusChoices


class DepartmentSerializerTest(TestCase):
    def setUp(self):
        manager = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            is_manager=True,
        )
        employee = Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
            address="456 Elm St",
            is_manager=False,
        )
        deleted_manager = Employee.objects.create(
            first_name="Bob",
            last_name="Brown",
            address="789 Oak St",
            is_manager=True,
            deleted_at="2023-10-01T00:00:00Z",
        )
        self.valid_data = {
            "name": "HR",
            "manager_id": manager.id,
        }
        self.invalid_data = {
            "name": "",
            "manager_id": None,
        }
        self.invalid_manager_data = {
            "name": "HR",
            "manager_id": employee.id,
        }
        self.invalid_deleted_manager_data = {
            "name": "HR",
            "manager_id": deleted_manager.id,
        }
        self.serializer = DepartmentSerializer(data=self.valid_data)

    def test_should_return_success_when_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())
        self.assertEqual(
            self.serializer.validated_data["name"], self.valid_data["name"]
        )
        self.assertEqual(
            self.serializer.validated_data["manager"].id, self.valid_data["manager_id"]
        )

    def test_should_return_err_when_invalid_serializer(self):
        serializer = DepartmentSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("manager_id", serializer.errors)
        self.assertEqual(serializer.errors["name"], ["This field may not be blank."])
        self.assertEqual(
            serializer.errors["manager_id"], ["This field may not be null."]
        )

    def test_should_return_err_when_manager_is_not_manager(self):
        serializer = DepartmentSerializer(data=self.invalid_manager_data)
        serializer.is_valid()
        self.assertIn("manager_id", serializer.errors)
        self.assertEqual(
            serializer.errors["manager_id"],
            ["This employee is not marked as a manager."],
        )

    def test_should_return_err_when_manager_is_deleted(self):
        serializer = DepartmentSerializer(data=self.invalid_deleted_manager_data)
        serializer.is_valid()
        self.assertIn("manager_id", serializer.errors)
        self.assertEqual(serializer.errors["manager_id"], ["This employee is deleted."])


class EmployeeSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "is_manager": True,
            "status_id": 1,
        }
        self.invalid_data = {
            "first_name": "",
            "last_name": "",
            "address": "",
            "is_manager": True,
            "status_id": None,
        }
        self.serializer = EmployeeSerializer(data=self.valid_data)

    def test_should_return_success_when_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())
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
            self.serializer.validated_data["is_manager"], self.valid_data["is_manager"]
        )
        self.assertEqual(
            self.serializer.validated_data["status"].id, self.valid_data["status_id"]
        )

    def test_should_return_err_when_invalid_serializer(self):
        serializer = EmployeeSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)
        self.assertIn("address", serializer.errors)
        self.assertIn("status_id", serializer.errors)
        self.assertEqual(
            serializer.errors["first_name"], ["This field may not be blank."]
        )
        self.assertEqual(
            serializer.errors["last_name"], ["This field may not be blank."]
        )
        self.assertEqual(serializer.errors["address"], ["This field may not be blank."])
        self.assertEqual(
            serializer.errors["status_id"], ["This field may not be null."]
        )


class PositionSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Software Engineer",
            "salary": 70000.0,
        }
        self.invalid_data = {
            "name": "",
            "salary": "",
        }
        self.serializer = PositionSerializer(data=self.valid_data)

    def test_should_return_success_when_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())
        self.assertEqual(
            self.serializer.validated_data["name"], self.valid_data["name"]
        )
        self.assertEqual(
            self.serializer.validated_data["salary"],
            self.valid_data["salary"],
        )

    def test_should_return_err_when_invalid_serializer(self):
        serializer = PositionSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("salary", serializer.errors)
        self.assertEqual(serializer.errors["name"], ["This field may not be blank."])
        self.assertEqual(serializer.errors["salary"], ["A valid number is required."])


class StatusSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": StatusChoices.CONTRACT,
        }
        self.invalid_data = {
            "name": "Test",
        }
        self.serializer = StatusSerializer(data=self.valid_data)

    def test_should_return_success_when_valid_serializer(self):
        self.assertTrue(self.serializer.is_valid())
        self.assertEqual(
            self.serializer.validated_data["name"], self.valid_data["name"]
        )

    def test_should_return_err_when_invalid_serializer(self):
        serializer = StatusSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertEqual(serializer.errors["name"], ['"Test" is not a valid choice.'])
