from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from organization.models import Organization
from organization.serializers import OrganizationSerializer
from utils.api_exceptions import CustomApiException


@api_view(['POST'])
def create_organization(request: HttpRequest):
    try:
        organization_serializer = OrganizationSerializer(data=request.data)
        organization_serializer.is_valid(raise_exception=True)
        organization_serializer.save()

        return Response(organization_serializer.data)
    except ValidationError:
        raise CustomApiException(400, 'Enter valid details')


@api_view(['GET', 'PUT'])
def do_organization(request: HttpRequest, organization_id):

    if request.method == 'GET':
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            organization = Organization.objects.get(
                organization_id=organization_id, email=email, active=True
            )

            print(organization.password)
            print(make_password('admin'))

            organization_serializer = OrganizationSerializer(organization)

            return Response(organization_serializer.data)
        except Organization.DoesNotExist:
            raise CustomApiException(400, 'Enter valid credentials')
        except ValidationError:
            raise CustomApiException(400, 'Enter valid details')

    if request.method == 'PUT':
        try:
            organization = Organization.objects \
                .get(organization_id=organization_id)
            organization_serializer = OrganizationSerializer(
                instance=organization, data=request.data, partial=True
            )

            organization_serializer.is_valid(raise_exception=True)
            organization_serializer.save()

            return Response(organization_serializer.data)
        except Organization.DoesNotExist:
            raise CustomApiException(400, 'No such organization exist')
