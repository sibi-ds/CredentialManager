import uuid

from django.test import TestCase

from organization.models import Organization
from organization.service import organization_service
from utils.api_exceptions import CustomApiException


class OrganizationServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(
            name='ideas2it',
            email='admin@ideas2it.com', password='admin',
        )

    def test_create_organization(self):
        payload = {
            'name': 'element5',
            'email': 'admin@element5.com',
            'password': 'admin'
        }

        organization = organization_service.create_organization(payload)

        self.assertEqual(organization.get('organization_id'), 2)
        self.assertEqual(organization.get('name'), 'element5')
        self.assertEqual(organization.get('email'), 'admin@element5.com')

        with self.assertRaises(CustomApiException):
            organization_service.create_organization({'name': 'ideas2it'})

        with self.assertRaises(CustomApiException):
            organization_service.create_organization(
                {'email': 'admin@ideas2it.com'}
            )

        with self.assertRaises(CustomApiException):
            organization_service.create_organization({'password': 'sibi'})

    def test_get_organizations(self):
        organizations = organization_service.get_organizations()

        self.assertTrue(len(organizations) == 1)
        self.assertEqual(organizations[0].get('organization_id'), 1)
        self.assertEqual(organizations[0].get('name'), 'ideas2it')
        self.assertEqual(organizations[0].get('email'), 'admin@ideas2it.com')

    def test_get_organization(self):
        existing_organization = Organization.objects.get(organization_id=1)

        organization = organization_service.get_organization(
            existing_organization.organization_uid,
            {'email': 'admin@ideas2it.com'}
        )

        self.assertEqual(organization.get('organization_id'), 1)
        self.assertEqual(organization.get('name'), 'ideas2it')
        self.assertEqual(organization.get('email'), 'admin@ideas2it.com')

        with self.assertRaises(CustomApiException):
            organization_service.get_organization(
                existing_organization.organization_uid, dict()
            )

        with self.assertRaises(CustomApiException):
            organization_service.get_organization(
                uuid.uuid4(), dict()
            )

    def test_update_organization(self):
        existing_organization = Organization.objects.get(organization_id=1)

        payload = {
            'name': 'element5',
            'email': 'admin@ideas2it.com'
        }

        updated_organization = organization_service.update_organization(
            existing_organization.organization_uid, payload
        )

        self.assertEqual(updated_organization.get('organization_id'), 1)
        self.assertEqual(updated_organization.get('name'), 'element5')
        self.assertEqual(updated_organization.get('email'),
                         'admin@ideas2it.com')

        with self.assertRaises(CustomApiException):
            organization_service.update_organization(
                uuid.uuid4(), payload
            )

        with self.assertRaises(CustomApiException):
            organization_service.update_organization(
                existing_organization.organization_uid, {}
            )

    def test_organization_status_update(self):
        existing_organization = Organization.objects.get(organization_id=1)

        payload = {
            'email': 'admin@ideas2it.com'
        }

        updated_organization = organization_service.update_organization_status(
            existing_organization.organization_uid, payload
        )

        self.assertEqual(updated_organization.get('organization_id'), 1)
        self.assertEqual(updated_organization.get('name'), 'ideas2it')
        self.assertEqual(updated_organization.get('active'), False)
        self.assertEqual(updated_organization.get('email'),
                         'admin@ideas2it.com')

        with self.assertRaises(CustomApiException):
            organization_service.update_organization(
                uuid.uuid4(), {}
            )

        with self.assertRaises(CustomApiException):
            organization_service.update_organization(
                existing_organization.organization_uid, {}
            )
