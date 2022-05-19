from django.test import TestCase

from employee.models import Employee

from organization.models import Organization


class EmployeeView(TestCase):

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

    def test_create_employee(self):
        employee = Employee.objects.get(employee_id=1)
        print(employee)

        self.assertTrue(isinstance(employee, Employee))
        self.assertEqual(employee.employee_id, 1)
        self.assertEqual(employee.name, 'sibi')
        self.assertEqual(employee.email, 'sibi@ideas2it.com')
        self.assertEqual(employee.password, 'sibi')
        self.assertEqual(employee.organization.organization_id, 1)
