"""this module is used to create, update and get operations on organizations
"""
import logging

from django.db import IntegrityError

from rest_framework.exceptions import ValidationError

from organization.models import Organization
from organization.serializers import OrganizationSerializer

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_organization(data):
    """used to create organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{create_organization.__name__} method')

        organization_serializer = OrganizationSerializer(data=data)
        organization_serializer.is_valid(raise_exception=True)
        organization_serializer.save()

        logger.debug('Organization creation successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_organization.__name__} method')

        return organization_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Organization creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_organization.__name__} method')
        raise CustomApiException(400, message)


def get_organizations():
    """used to get all organizations
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{get_organizations.__name__} method')

        organizations = Organization.objects.filter(active=True)
        organization_serializer = OrganizationSerializer(organizations,
                                                         many=True)

        logger.debug(f'Exit {__name__} module, '
                     f'{get_organizations.__name__} method')

        return organization_serializer.data
    except IntegrityError:
        logger.error('Organizations fetch failure')
        logger.error(f'Exit {__name__} module, '
                     f'{get_organizations.__name__} method')
        raise CustomApiException(500, 'Organizations fetch failure')


def get_organization(organization_uid, data):
    """used to get an organization details
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{get_organization.__name__} method')

        email = data['email']

        organization = Organization.objects.get(
            organization_uid=organization_uid, email=email, active=True
        )

        organization_serializer = OrganizationSerializer(organization)

        logger.debug('Organization fetch successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{get_organization.__name__} method')

        return organization_serializer.data
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_organization.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{get_organization.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{get_organization.__name__} method')
        raise CustomApiException(400, message)


def update_organization(organization_uid, data):
    """used to update organization details
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{update_organization.__name__} method')

        email = data["email"]

        organization = Organization.objects.get(
            organization_uid=organization_uid,
            email=email, active=True
        )

        organization_serializer = OrganizationSerializer(
            instance=organization, data=data, partial=True
        )

        organization_serializer.is_valid(raise_exception=True)
        organization_serializer.save()

        logger.debug('Organization update successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_organization.__name__} method')

        return organization_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Organization update failure')
        logger.error(f'Exit {__name__} module, '
                     f'{update_organization.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{update_organization.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_organization.__name__} method')
        raise CustomApiException(400, 'No such organization exist')


def update_organization_status(organization_uid, data):
    """used to update organization status
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{update_organization_status.__name__} method')

        email = data['email']

        organization = Organization.objects.get(
            organization_uid=organization_uid,
            email=email
        )

        organization.active = not organization.active
        organization.save()

        organization_serializer = OrganizationSerializer(organization)

        logger.debug('Organization status updated successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_organization_status.__name__} method')

        return organization_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Organization status update failure')
        logger.error(f'Exit {__name__} module, '
                     f'{update_organization_status.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{update_organization_status.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_organization_status.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
