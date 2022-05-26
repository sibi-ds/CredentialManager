"""this module is used to call create, update and get methods on organizations
"""
import logging

from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from organization.service import organization_service

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST'])
def create_organization(request: HttpRequest):
    """used to create organization
    """
    try:
        logger.debug(f'Enter {__name__} module, create_organization method')
        organization_serializer = organization_service \
            .create_organization(request.data)
        logger.debug(f'Exit {__name__} module, create_organization method')
        return Response(organization_serializer)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_organization method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET'])
def get_organizations(request: HttpRequest):
    """used to get all organizations
    """
    try:
        logger.debug(f'Enter {__name__} module, get_organizations method')
        organization_serializer = organization_service.get_organizations()
        logger.debug(f'Exit {__name__} module, get_organizations method')
        return Response(organization_serializer)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, get_organizations method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT'])
def do_organization(request: HttpRequest, organization_uid):
    logger.debug(f'Enter {__name__} module, do_organization method')

    if request.method == 'GET':
        """used to get an organization details
        """
        try:
            organization_serializer = organization_service \
                .get_organization(organization_uid, request.data)
            logger.debug(f'Exit {__name__} module, do_organization method')
            return Response(organization_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_organization method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        """used to update organization details
        """
        try:
            organization_serializer = organization_service \
                .update_organization(organization_uid, request.data)
            logger.debug(f'Exit {__name__} module, do_organization method')
            return Response(organization_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_organization method')
            raise CustomApiException(e.status_code, e.detail)
