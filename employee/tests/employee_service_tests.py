from unittest import mock

from django.test import TestCase

from employee.models import Employee
from employee.service import employee_service

from organization.models import Organization


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
