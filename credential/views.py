"""This module is used to call operations on
vaults. components, item and usr accesses
"""
import logging

from django.contrib.auth.hashers import make_password
from django.http import HttpRequest

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from credential.models import Project, Vault
from credential.serializers import VaultSerializer
from project.serializers import ProjectSerializer

from credential.service import component_service
from credential.service import user_access_service
from credential.service import vault_service

from credential.utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


@api_view(['POST'])
def create_vault(request: HttpRequest):
    logger.info(f'Enter {__name__} module, {create_vault.__name__} method')

    try:
        vault = vault_service.create_vault(request.data)
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        return Response(vault)
    except CustomApiException as e:
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes((IsAuthenticated, ))
def do_vault(request: HttpRequest, vault_id):
    logger.info(f'Enter {__name__} module, {do_vault.__name__} method')

    if request.method == 'GET':
        try:
            vault = vault_service.get_vault(vault_id, request.data)
            logger.info(f'Exit {__name__} module, {do_vault.__name__} method')
            return Response(vault)
        except CustomApiException as e:
            logger.info(f'Exit {__name__} module, {do_vault.__name__} method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        try:
            vault = vault_service.update_vault(vault_id, request.data)
            logger.info(f'Exit {__name__} module, {do_vault.__name__} method')
            return Response(vault)
        except CustomApiException as e:
            logger.info(f'Exit {__name__} module, {do_vault.__name__} method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        try:
            vault_active_status = vault_service \
                .change_active_status(vault_id, request.data)
            logger.info(f'Exit {__name__} module, {do_vault.__name__} method')
            return Response(f'Active status changes to {vault_active_status}')
        except CustomApiException as e:
            logger.info(f'Exit {__name__} module, {do_vault.__name__} method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def create_component(request: HttpRequest, vault_id):
    logger.info(f'Enter {__name__} module, {create_component.__name__} method')

    try:
        component = component_service.create_component(vault_id, request.data)
        logger.info(f'Exit {__name__} module, '
                    f'{create_component.__name__} method')
        return Response(component)
    except CustomApiException as e:
        logger.info(f'Exit {__name__} module, '
                    f'{create_component.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT', 'PATCH'])
def do_component(request: HttpRequest, vault_id, component_id):
    logger.info(f'Enter {__name__} module, {do_component.__name__} method')

    if request.method == 'GET':
        try:
            component = component_service.get_component(vault_id, component_id,
                                                        request.data)
            logger.info(f'Exit {__name__} module,'
                        f'{do_component.__name__} method')
            return Response(component)
        except CustomApiException as e:
            logger.info(f'Exit {__name__} module,'
                        f'{do_component.__name__} method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        try:
            component = component_service.update_component(vault_id,
                                                           component_id,
                                                           request.data)
            logger.info(f'Exit {__name__} module, '
                        f'{do_component.__name__} method')
            return Response(component)
        except CustomApiException as e:
            logger.info(f'Exit {__name__} module, '
                        f'{do_component.__name__} method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        try:
            component_active_status = component_service \
                .change_active_status(vault_id, component_id, request.data)
            logger.info(f'Exit {__name__} module, '
                        f'{do_component.__name__} method')
            return Response(f'Active status changed '
                            f'to {component_active_status}')
        except CustomApiException as e:
            logger.info(f'Exit {__name__} module, '
                        f'{do_component.__name__} method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST', 'PUT', 'PATCH'])
def do_vault_access(request: HttpRequest, vault_id):
    logger.info(f'Enter {__name__} module, {do_vault_access.__name__} method')

    if request.method == 'POST':
        try:
            vault_access = user_access_service \
                .create_vault_access(vault_id, request.data)
            logger.info(f'Exit {__name__} module, '
                        f'{do_vault_access.__name__} method')
            return Response(vault_access)
        except CustomApiException as e:
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        try:
            return user_access_service.remove_vault_access(vault_id,
                                                           request.data)
        except CustomApiException as e:
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST', 'PUT', 'PATCH'])
def do_component_access(request: HttpRequest, vault_id, component_id):
    logger.info(f'Enter {__name__} module, '
                f'{do_component_access.__name__} method')

    if request.method == 'POST':
        component_access = user_access_service.create_component_access(
            vault_id, component_id, request.data)
        logger.info(f'Exit {__name__} module, '
                    f'{do_component_access.__name__} method')
        return Response(component_access)

    if request.method == 'PATCH':
        try:
            return user_access_service.remove_component_access(vault_id,
                                                               component_id,
                                                               request.data)
        except CustomApiException as e:
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def get(request):
    email = request.data.get('email')
    password = request.data.get('password')
    # password = make_password(password)
    vault = Vault.objects.get(email=email, password=password)

    return Response(VaultSerializer(vault).data)
