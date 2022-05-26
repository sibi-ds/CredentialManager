from unittest import TestCase

from django.http import HttpRequest

from organization import views


class TestOrganizationView(TestCase):

    def test_create_organization(self):
        payload = {
            'organization_id': 3,
            'name': 'ideas2it1',
            'email': 'admin@ideas2it1.com',
            'password': 'admin'
        }

        request = HttpRequest(mutable=True)
        request.POST = payload
        request.method = 'POST'
        request.content_type = 'application/json'

        print(request, request.POST)

        response = views.create_organization(request)

        print(response)

