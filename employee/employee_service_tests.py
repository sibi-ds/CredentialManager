from django.test import TestCase
# from unittest import TestCase
from unittest.mock import patch

from employee.models import Employee
from employee.service import employee_service

from organization.models import Organization


class TestEmployeeService(TestCase):

    @classmethod
    def setUpTestData(cls):
        organization = Organization.objects.create(
            organization_id=1, name='ideas2it',
            email='admin@ideas2it.com', password='admin'
        )

        Employee.objects.create(
            employee_id=1, name='sibi',
            email='sibi@ideas2it.com', password='sibi',
            created_by=organization,
            organization=organization
        )

    def test_create_employee(self):
        payload = {
            'employee_id': 7,
            'name': 's',
            'email': 's@ideas2it.com',
            'password': 's'
        }

        response = employee_service.create_employee(1, payload)

        print(response)

