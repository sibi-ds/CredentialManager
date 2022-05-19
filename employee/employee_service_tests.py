from unittest import mock
from unittest.mock import MagicMock, patch

from django.test import TestCase

from employee.models import Employee
from employee.service import employee_service
from employee.serializers import EmployeeSerializer

from organization.models import Organization


class EmployeeServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        organization = Organization.objects.create(
            organization_id=1, name='ideas2it',
            email='admin@ideas2it.com', password='admin',
        )

        employee = Employee.objects.create(
            employee_id=1, name='sibi',
            email='sibi@ideas2it.com', password='sibi',
            organization=organization,
            created_by=organization
        )

    # @mock.patch('employee.models.Employee.save',
    #             return_value=Employee.objects.filter(employee_id=1).first())
    @mock.patch('employee.models.Employee.objects.create',
                return_value=Employee.objects.filter(employee_id=1))
    def test_create_employees(self, mocked_create_employee,
                              ):
        print(mocked_create_employee.return_value)

        payload = {
            'employee_id': 1,
            'name': 'sibi1',
            'email': 'sibi1@ideas2it.com',
            'password': 'sibi1',
        }

        # response = employee_service.create_employee(1, payload)
        response = Employee.objects.create(dict())
        print(response)
