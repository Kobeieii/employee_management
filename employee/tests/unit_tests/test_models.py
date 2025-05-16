from django.test import TestCase
from django.db import DataError, IntegrityError
from employee.models.department import Department
from employee.models.employee import Employee
from employee.models.position import Position
from employee.models.status import Status, StatusChoices


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.name = "HR"
        self.manager = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Main St",
            is_manager=True,
        )

    def test_should_return_success_when_creating_department(self):
        department = Department.objects.create(
            name="HR",
            manager=self.manager,
        )
        self.assertEqual(department.name, "HR")
        self.assertEqual(department.manager, self.manager)

    def test_should_return_success_when_deleting_department(self):
        department = Department.objects.create(
            name="HR",
            manager=self.manager,
        )
        department.delete()
        self.assertIsNotNone(department.deleted_at)

    def test_should_return_err_when_creating_duplicate_department(self):
        Department.objects.create(
            name=self.name,
            manager=self.manager,
        )
        with self.assertRaises(IntegrityError):
            Department.objects.create(
                name=self.name,
                manager=self.manager,
            )

    def test_should_return_err_when_name_is_over_125_chars(self):
        long_name = "A" * 126
        with self.assertRaises(DataError):
            Department.objects.create(
                name=long_name,
                manager=self.manager,
            )

    def test_should_return_err_when_name_is_none(self):
        with self.assertRaises(IntegrityError):
            Department.objects.create(
                name=None,
                manager=self.manager,
            )

    def test_should_return_err_when_manager_is_none(self):
        with self.assertRaises(IntegrityError):
            Department.objects.create(
                name="Engineering",
                manager=None,
            )


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.first_name = "Jane"
        self.last_name = "Doe"
        self.address = "456 Elm St"
        self.is_manager = False

    def test_should_return_success_when_creating_employee(self):
        employee = Employee.objects.create(
            first_name="Alice",
            last_name="Smith",
            address="789 Oak St",
            is_manager=True,
        )
        self.assertEqual(employee.first_name, "Alice")
        self.assertEqual(employee.last_name, "Smith")
        self.assertEqual(employee.address, "789 Oak St")
        self.assertTrue(employee.is_manager)

    def test_should_return_success_when_creating_employee_with_default_is_manager(self):
        employee = Employee.objects.create(
            first_name="Bob",
            last_name="Brown",
            address="101 Pine St",
        )
        self.assertEqual(employee.first_name, "Bob")
        self.assertEqual(employee.last_name, "Brown")
        self.assertEqual(employee.address, "101 Pine St")
        self.assertFalse(employee.is_manager)

    def test_should_return_success_when_creating_employee_with_default_status(self):
        employee = Employee.objects.create(
            first_name="Charlie",
            last_name="Green",
            address="202 Maple St",
        )
        status_id = Status.get_default_status()
        self.assertEqual(employee.first_name, "Charlie")
        self.assertEqual(employee.last_name, "Green")
        self.assertEqual(employee.address, "202 Maple St")
        self.assertEqual(employee.status.id, status_id)

    def test_should_return_success_when_deleting_employee(self):
        employee = Employee.objects.create(
            first_name="David",
            last_name="White",
            address="303 Birch St",
        )
        employee.delete()
        self.assertIsNotNone(employee.deleted_at)

    def test_should_return_err_when_creating_duplicate_employee(self):
        Employee.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            address=self.address,
            is_manager=self.is_manager,
        )
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name=self.first_name,
                last_name=self.last_name,
                address=self.address,
                is_manager=self.is_manager,
            )

    def test_should_return_err_when_first_name_is_over_125_chars(self):
        long_first_name = "A" * 126
        with self.assertRaises(DataError):
            Employee.objects.create(
                first_name=long_first_name,
                last_name="Doe",
                address="123 Main St",
                is_manager=False,
            )

    def test_should_return_err_when_last_name_is_over_125_chars(self):
        long_last_name = "A" * 126
        with self.assertRaises(DataError):
            Employee.objects.create(
                first_name="Jane",
                last_name=long_last_name,
                address="123 Main St",
                is_manager=False,
            )

    def test_should_return_err_when_address_is_none(self):
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name="Jane",
                last_name="Doe",
                address=None,
                is_manager=False,
            )

    def test_should_return_err_when_first_name_is_none(self):
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name=None,
                last_name="Doe",
                address="123 Main St",
                is_manager=False,
            )

    def test_should_return_err_when_last_name_is_none(self):
        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                first_name="Jane",
                last_name=None,
                address="123 Main St",
                is_manager=False,
            )


class PositionModelTest(TestCase):
    def setUp(self):
        self.name = "Software Engineer"
        self.salary = 70000.0

    def test_should_return_success_when_creating_position(self):
        position = Position.objects.create(
            name=self.name,
            salary=self.salary,
        )
        self.assertEqual(position.name, self.name)
        self.assertEqual(position.salary, self.salary)

    def test_should_return_success_when_deleting_position(self):
        position = Position.objects.create(
            name=self.name,
            salary=self.salary,
        )
        position.delete()
        self.assertIsNotNone(position.deleted_at)

    def test_should_return_err_when_creating_duplicate_position(self):
        Position.objects.create(
            name=self.name,
            salary=self.salary,
        )
        with self.assertRaises(IntegrityError):
            Position.objects.create(
                name=self.name,
                salary=self.salary,
            )

    def test_should_return_err_when_name_is_over_125_chars(self):
        long_name = "A" * 126
        with self.assertRaises(DataError):
            Position.objects.create(
                name=long_name,
                salary=self.salary,
            )

    def test_should_return_err_when_salary_is_none(self):
        with self.assertRaises(IntegrityError):
            Position.objects.create(
                name="Data Scientist",
                salary=None,
            )


class StatusModelTest(TestCase):
    def test_should_return_success_when_creating_status(self):
        status = Status.objects.create(name=StatusChoices.RETIRED)
        self.assertEqual(status.name, StatusChoices.RETIRED)

    def test_should_return_success_when_default_status_eq_normal_status(self):
        status_id = Status.get_default_status()
        status = Status.objects.get(name=StatusChoices.NORMAL)
        self.assertEqual(status_id, status.id)

    def test_should_return_success_when_deleting_status(self):
        status = Status.objects.create(name=StatusChoices.RETIRED)
        status.delete()
        self.assertIsNotNone(status.deleted_at)

    def test_should_return_err_when_creating_duplicate_status(self):
        Status.objects.create(name=StatusChoices.RETIRED)
        with self.assertRaises(IntegrityError):
            Status.objects.create(name=StatusChoices.RETIRED)

    def test_should_return_err_when_name_is_over_20_chars(self):
        long_name = "A" * 21
        with self.assertRaises(DataError):
            Status.objects.create(name=long_name)

    def test_should_return_err_when_name_is_none(self):
        with self.assertRaises(IntegrityError):
            Status.objects.create(name=None)
