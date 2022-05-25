import uuid
from unittest import mock

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

    @mock.patch('organization.models.Organization.objects.all',
                return_value=Organization.objects.all())
    def test_get_organizations(self, mocked_get_organizations):
        organizations = organization_service.get_organizations()

        self.assertTrue(
            len(organizations) == len(mocked_get_organizations.return_value)
        )
        self.assertEqual(
            organizations[0].get('organization_id'),
            mocked_get_organizations.return_value[0].organization_id
        )
        self.assertEqual(
            organizations[0].get('name'),
            mocked_get_organizations.return_value[0].name
        )
        self.assertEqual(
            organizations[0].get('email'),
            mocked_get_organizations.return_value[0].email
        )

    @mock.patch('organization.models.Organization.objects.get',
                return_value=Organization.objects.get(organization_id=1))
    def test_get_organization(self, mocked_get_organization):
        organization = organization_service.get_organization(uuid.uuid4(),
                                                             dict())

        self.assertEqual(organization.get('organization_id'),
                         mocked_get_organization.return_value.organization_id)
        self.assertEqual(organization.get('name'),
                         mocked_get_organization.return_value.name)
        self.assertEqual(organization.get('email'),
                         mocked_get_organization.return_value.email)

    @mock.patch('organization.models.Organization.objects.get',
                return_value=Organization.objects.get(organization_id=1))
    def test_update_organization(self, mocked_get_organization):
        payload = {
            'name': 'element5',
            'email': 'admin@element5.com'
        }

        updated_organization = organization_service.update_organization(
            uuid.uuid4(), payload
        )

        self.assertEqual(updated_organization.get('organization_id'), 1)
        self.assertEqual(updated_organization.get('name'), 'element5')
        self.assertEqual(updated_organization.get('email'),
                         'admin@element5.com')
