"""This module is used to call operations on
vaults, components, items and user accesses
"""
import logging

from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from credential.service import component_service
from credential.service import user_access_service
from credential.service import vault_service

from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


@api_view(['POST'])
def create_vault(request: HttpRequest, uid):
    logger.debug(f'Enter {__name__} module, create_vault method')

    try:
        organization_id = request.query_params.get('organization_id')
        vault = vault_service.create_vault(organization_id, uid, request.data)
        logger.debug(f'Exit {__name__} module, create_vault method')
        return Response(vault)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_vault method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT'])
def do_vault(request: HttpRequest, uid, vault_id):
    logger.debug(f'Enter {__name__} module, do_vault method')

    organization_id = request.query_params.get('organization_id')

    if request.method == 'GET':
        try:
            vault = vault_service.get_vault(organization_id, uid, vault_id)
            logger.debug(f'Exit {__name__} module, do_vault method')
            return Response(vault)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_vault method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        try:
            vault = vault_service.update_vault(organization_id, uid, vault_id,
                                               request.data)
            logger.debug(f'Exit {__name__} module, do_vault method')
            return Response(vault)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_vault method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def create_component(request: HttpRequest, uid, vault_id):
    logger.debug(f'Enter {__name__} module, create_component method')

    try:
        organization_id = request.query_params.get('organization_id')
        component = component_service.create_component(organization_id, uid,
                                                       vault_id, request.data)
        logger.debug(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        return Response(component)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT'])
def do_component(request: HttpRequest, uid, vault_id, component_id):
    logger.debug(f'Enter {__name__} module, do_component method')

    organization_id = request.query_params.get('organization_id')

    if request.method == 'GET':
        try:
            component = component_service.get_component(organization_id, uid,
                                                        vault_id, component_id,
                                                        request.data)
            logger.debug(f'Exit {__name__} module,'
                         f'{do_component.__name__} method')
            return Response(component)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module,'
                         f'{do_component.__name__} method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        try:
            component = component_service.update_component(organization_id,
                                                           uid,
                                                           vault_id,
                                                           component_id,
                                                           request.data)
            logger.debug(f'Exit {__name__} module, '
                         f'{do_component.__name__} method')
            return Response(component)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, '
                         f'{do_component.__name__} method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def create_vault_access(request: HttpRequest, uid, vault_id):
    logger.debug(f'Enter {__name__} module, create_vault_access method')

    organization_id = request.query_params.get('organization_id')

    try:
        vault_access = user_access_service.create_vault_access(
            organization_id, uid, vault_id, request.data
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{do_vault_access.__name__} method')
        return Response(vault_access)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, '
                     f'{do_vault_access.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['PUT', 'DELETE'])
def do_vault_access(request: HttpRequest, uid, vault_id, vault_access_id):
    logger.debug(f'Enter {__name__} module, do_vault_access method')

    organization_id = request.query_params.get('organization_id')

    if request.method == 'PUT':
        try:
            vault_access = user_access_service.update_vault_access(
                organization_id, uid, vault_id, vault_access_id, request.data
            )

            logger.debug(f'Exit {__name__} module, '
                         f'{do_vault_access.__name__} method')
            return Response(vault_access)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, '
                         f'{do_vault_access.__name__} method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'DELETE':
        try:
            vault_access = user_access_service.delete_vault_access(
                organization_id, uid, vault_id, vault_access_id
            )

            logger.debug(f'Exit {__name__} module, '
                         f'{do_vault_access.__name__} method')
            return Response(vault_access)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, '
                         f'{do_vault_access.__name__} method')
            raise CustomApiException(e.status_code, e.detail)
