import logging

from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from organization.models import Organization
from organization.serializers import OrganizationSerializer

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST'])
def create_organization(request: HttpRequest):
    try:
        logger.debug(f'Enter {__name__} module, create_organization method')

        organization_serializer = OrganizationSerializer(data=request.data)
        organization_serializer.is_valid(raise_exception=True)
        organization_serializer.save()

        logger.debug('Organization creation successful')
        logger.debug(f'Exit {__name__} module, create_organization method')

        return Response(organization_serializer.data)
    except ValidationError:
        logger.error('Organization creation failure')
        logger.error(f'Exit {__name__} module, create_organization method')
        raise CustomApiException(400, 'Enter valid details')


@api_view(['GET', 'PUT'])
def do_organization(request: HttpRequest, organization_id):
    logger.debug(f'Enter {__name__} module, do_organization method')

    if request.method == 'GET':
        try:
            email = request.data.get("email")

            organization = Organization.objects.get(
                organization_id=organization_id, email=email, active=True
            )

            organization_serializer = OrganizationSerializer(organization)

            logger.debug('Organization fetch successful')

            return Response(organization_serializer.data)
        except Organization.DoesNotExist:
            logger.error('No such organization exist.'
                         'Organization creation failure')
            logger.error(f'Exit {__name__} module, do_organization method')
            raise CustomApiException(400, 'Enter valid credentials')
        except ValidationError:
            logger.error('Enter valid details.Organization creation failure')
            logger.error(f'Exit {__name__} module, do_organization method')
            raise CustomApiException(400, 'Enter valid details')

    if request.method == 'PUT':
        try:
            email = request.data.get("email")

            organization = Organization.objects.get(
                organization_id=organization_id,
                email=email
            )

            organization_serializer = OrganizationSerializer(
                instance=organization, data=request.data, partial=True
            )

            organization_serializer.is_valid(raise_exception=True)
            organization_serializer.save()

            logger.debug('Organization update successful')

            return Response(organization_serializer.data)
        except ValidationError:
            logger.error('Enter valid details.Organization creation failure')
            logger.error(f'Exit {__name__} module, do_organization method')
            raise CustomApiException(400, 'Enter valid details')
        except Organization.DoesNotExist:
            logger.error('No such organization exist.'
                         'Organization creation failure')
            logger.error(f'Exit {__name__} module, do_organization method')
            raise CustomApiException(400, 'No such organization exist')
