import uuid
from unittest import mock

from django.test import TestCase

from employee.models import Employee
from employee.service import employee_service

from organization.models import Organization
from utils.api_exceptions import CustomApiException


class EmployeeServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        organization = Organization.objects.create(
            name='ideas2it',
            email='admin@ideas2it.com', password='admin',
        )

        employee = Employee.objects.create(
            name='sibi',
            email='sibi@ideas2it.com', password='sibi',
            organization=organization,
            created_by=organization
        )

    def test_create_employee(self):
        payload = {
            'name': 'sasi',
            'email': 'sasi@ideas2it.com',
            'password': 'sasi',
        }

        employee = employee_service.create_employee(1, payload)

        self.assertEqual(employee.get('employee_id'), 2)
        self.assertEqual(employee.get('name'), 'sasi')
        self.assertEqual(employee.get('email'), 'sasi@ideas2it.com')
        self.assertEqual(employee.get('organization'), 1)

        with self.assertRaises(CustomApiException):
            employee_service.create_employee(1, {})

        with self.assertRaises(CustomApiException):
            employee_service.create_employee(2, {})

    def test_get_employee(self):
        payload = {
            'email': 'sibi@ideas2it.com'
        }

        employee = employee_service.get_employee(1, payload)

        self.assertEqual(employee.get('organization'), 1)
        self.assertEqual(employee.get('employee_id'), 1)
        self.assertEqual(employee.get('name'), 'sibi')
        self.assertEqual(employee.get('email'), 'sibi@ideas2it.com')

    def test_get_employees(self):
        payload = {
            'email': 'admin@ideas2it.com'
        }

        employees = employee_service.get_employees(1, payload)

        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].get('organization'), 1)
        self.assertEqual(employees[0].get('employee_id'), 1)
        self.assertEqual(employees[0].get('name'), 'sibi')
        self.assertEqual(employees[0].get('email'), 'sibi@ideas2it.com')

        with self.assertRaises(CustomApiException):
            employee_service.get_employees(1, {})

        with self.assertRaises(CustomApiException):
            employee_service.get_employees(2, {'email': 'admin@idesa2it.com'})

    def test_update_employee(self):
        existing_employee = Employee.objects.get(employee_id=1)

        payload = {
            'name': 'sibi dhanapal',
            'email': 'sibi@ideas2it.com',
            'password': 'sibi dhanapal',
        }

        employee = employee_service.update_employee(
            1, existing_employee.employee_uid, payload
        )

        self.assertEqual(employee.get('organization'), 1)
        self.assertEqual(employee.get('employee_id'), 1)
        self.assertEqual(employee.get('name'), 'sibi dhanapal')
        self.assertEqual(employee.get('email'), 'sibi@ideas2it.com')

        with self.assertRaises(CustomApiException):
            employee_service.update_employee(
                1, existing_employee.employee_uid, {}
            )

        with self.assertRaises(CustomApiException):
            employee_service.update_employee(
                2, existing_employee.employee_uid, {}
            )

        with self.assertRaises(CustomApiException):
            employee_service.update_employee(
                1, uuid.uuid4(), {}
            )
