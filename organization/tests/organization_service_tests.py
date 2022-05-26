from django.test import TestCase

from organization.models import Organization
from organization.service import organization_service


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

    def test_get_organizations(self):
        organizations = organization_service.get_organizations()

        self.assertTrue(len(organizations) == 1)
        self.assertEqual(organizations[0].get('organization_id'), 1)
        self.assertEqual(organizations[0].get('name'), 'ideas2it')
        self.assertEqual(organizations[0].get('email'), 'admin@ideas2it.com')

    def test_get_organization(self):
        organization = Organization.objects.get(organization_id=1)

        organization = organization_service.get_organization(
            organization.organization_uid,
            {'email': 'admin@ideas2it.com'}
        )

        self.assertEqual(organization.get('organization_id'), 1)
        self.assertEqual(organization.get('name'), 'ideas2it')
        self.assertEqual(organization.get('email'), 'admin@ideas2it.com')

    def test_update_organization(self):
        organization = Organization.objects.get(organization_id=1)

        payload = {
            'name': 'element5',
            'email': 'admin@ideas2it.com'
        }

        updated_organization = organization_service.update_organization(
            organization.organization_uid, payload
        )

        self.assertEqual(updated_organization.get('organization_id'), 1)
        self.assertEqual(updated_organization.get('name'), 'element5')
        self.assertEqual(updated_organization.get('email'),
                         'admin@ideas2it.com')
