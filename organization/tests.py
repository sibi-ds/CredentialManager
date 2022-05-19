from django.test import TestCase

from organization.models import Organization


class OrganizationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Organization.objects.create(
            organization_id=1, name='ideas2it',
            email='admin@ideas2it.com', password='admin',
        )

    def test_create_organization(self):
        payload = {
            'organization_id': 2,
            'name': 'element5',
            'email': 'admin@element5.com',
            'password': 'admin'
        }

        organization = Organization.objects.create(**payload)
        self.assertTrue(isinstance(organization, Organization))
        self.assertEqual(organization.organization_id, 2)
        self.assertEqual(organization.name, 'element5')
        self.assertEqual(organization.email, 'admin@element5.com')
        self.assertEqual(organization.password, 'admin')

    def test_get_organizations(self):
        organizations = Organization.objects.all()

        self.assertTrue(len(organizations) == 1)
        self.assertTrue(isinstance(organizations[0], Organization))
        self.assertEqual(organizations[0].organization_id, 1)
        self.assertEqual(organizations[0].name, 'ideas2it')
        self.assertEqual(organizations[0].email, 'admin@ideas2it.com')
        self.assertEqual(organizations[0].password, 'admin')

    def test_get_organization(self):
        organization = Organization.objects.get(organization_id=1)

        self.assertTrue(isinstance(organization, Organization))
        self.assertEqual(organization.organization_id, 1)
        self.assertEqual(organization.name, 'ideas2it')
        self.assertEqual(organization.email, 'admin@ideas2it.com')
        self.assertEqual(organization.password, 'admin')
