from unittest import mock

from django.test import TestCase
from credential.models import Vault
from credential.service import vault_service
from employee.models import Employee
from organization.models import Organization
from project.models import Project


class VaultServiceTest(TestCase):

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

        project = Project.objects.create(
            name='Ulab Systems',
            email='ulabsystems@ideas2it.com',
            description='Ulab Systems',
            organization=organization,
            created_by=organization
        )

        vault = Vault.objects.create(
            name='Organization Vault',
            description='Organization Vault',
            organization=organization,
            created_by=employee
        )

    def test_create_vault(self):
        employee = Employee.objects.get(employee_id=1)

        payload = {
            'name': 'Demo Vault',
            'description': 'Demo Vault'
        }

        vault = vault_service.create_vault(1, employee.employee_uid, payload)

        self.assertEqual(vault.get('vault_id'), 2)
        self.assertEqual(vault.get('name'), 'Demo Vault')
        self.assertEqual(vault.get('description'), 'Demo Vault')
        self.assertEqual(vault.get('organization'), 1)

    def test_update_vault(self):
        employee = Employee.objects.get(employee_id=1)
        vault = Vault.objects.get(vault_id=1)

        payload = {
            'name': 'Updated Demo Vault',
            'description': 'Updated Demo Vault'
        }

        vault = vault_service.update_vault(
            1, employee.employee_uid, vault.vault_uid, payload
        )

        self.assertEqual(vault.get('vault_id'), 1)
        self.assertEqual(vault.get('name'), 'Updated Demo Vault')
        self.assertEqual(vault.get('description'), 'Updated Demo Vault')

    def test_get_vault(self):
        employee = Employee.objects.get(employee_id=1)
        vault = Vault.objects.get(vault_id=1)

        vault = vault_service.get_vault(
            1, employee.employee_uid, vault.vault_uid
        )

        self.assertEqual(vault.get('vault_id'), 1)
        self.assertEqual(vault.get('name'), 'Organization Vault')
        self.assertEqual(vault.get('description'), 'Organization Vault')

    def test_get_vaults(self):
        payload = {
            'email': 'admin@ideas2it.com'
        }

        vaults = vault_service.get_vaults(1, payload)

        self.assertEqual(len(vaults), 1)
        self.assertEqual(vaults[0].get('vault_id'), 1)
        self.assertEqual(vaults[0].get('name'), 'Organization Vault')
        self.assertEqual(vaults[0].get('description'), 'Organization Vault')
