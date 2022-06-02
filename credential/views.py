"""This module is used to call operations on
vaults, components, items and user accesses
"""
import logging

from django.http import HttpRequest
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from credential.service import component_service, item_service
from credential.service import user_access_service
from credential.service import vault_service

from utils import encryptor
from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST'])
def create_vault(request: HttpRequest, employee_uid):
    logger.debug(f'Enter {__name__} module, create_vault method')

    try:
        organization_id = request.query_params.get('organization_id')
        vault = vault_service.create_vault(organization_id, employee_uid,
                                           request.data)
        logger.debug(f'Exit {__name__} module, create_vault method')
        return Response(vault)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_vault method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET'])
def get_vaults(request: HttpRequest):
    logger.debug(f'Enter {__name__} module, get_vaults method')

    try:
        organization_id = request.query_params.get('organization_id')
        vaults = vault_service.get_vaults(organization_id, request.data)
        logger.debug(f'Exit {__name__} module, get_vaults method')
        return Response(vaults)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, get_vaults method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT', 'PATCH'])
def do_vault(request: HttpRequest, employee_uid, vault_uid):
    logger.debug(f'Enter {__name__} module, do_vault method')

    organization_id = request.query_params.get('organization_id')

    if request.method == 'GET':
        try:
            vault = vault_service.get_vault(organization_id, employee_uid,
                                            vault_uid)
            logger.debug(f'Exit {__name__} module, do_vault method')
            return Response(vault)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_vault method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        try:
            vault = vault_service.update_vault(organization_id, employee_uid,
                                               vault_uid, request.data)
            logger.debug(f'Exit {__name__} module, do_vault method')
            return Response(vault)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_vault method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        """used to update vault status
        """
        try:
            vault_serializer = vault_service.update_vault_status(
                organization_id, employee_uid, vault_uid, request.data
            )
            logger.debug(f'Exit {__name__} module, do_vault method')
            return Response(vault_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_vault method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def create_component(request: HttpRequest, employee_uid, vault_uid):
    logger.debug(f'Enter {__name__} module, create_component method')

    try:
        organization_id = request.query_params.get('organization_id')
        component = component_service.create_component(organization_id,
                                                       employee_uid,
                                                       vault_uid,
                                                       request.data)
        logger.debug(f'Exit {__name__} module, create_component method')
        return Response(component)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_component method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT', 'PATCH'])
def do_component(request: HttpRequest, employee_uid, vault_uid, component_uid):
    logger.debug(f'Enter {__name__} module, do_component method')

    organization_id = request.query_params.get('organization_id')

    if request.method == 'GET':
        try:
            component = component_service.get_component(organization_id,
                                                        employee_uid,
                                                        vault_uid,
                                                        component_uid,
                                                        request.data)
            logger.debug(f'Exit {__name__} module, do_component method')
            return Response(component)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_component method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        try:
            component = component_service.update_component(organization_id,
                                                           employee_uid,
                                                           vault_uid,
                                                           component_uid,
                                                           request.data)
            logger.debug(f'Exit {__name__} module, do_component method')
            return Response(component)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_component method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        """used to update component status
        """
        try:
            component_serializer = component_service.update_component_status(
                organization_id, employee_uid,
                vault_uid, component_uid, request.data
            )
            logger.debug(f'Exit {__name__} module, do_component method')
            return Response(component_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_component method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def create_vault_access(request: HttpRequest, employee_uid, vault_uid):
    logger.debug(f'Enter {__name__} module, create_vault_access method')

    organization_id = request.query_params.get('organization_id')

    try:
        vault_access = user_access_service.create_vault_access(
            organization_id, employee_uid, vault_uid, request.data
        )

        logger.debug(f'Exit {__name__} module, create_vault_access method')
        return Response(vault_access)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_vault_access method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['PATCH'])
def remove_vault_access(request: HttpRequest, employee_uid, vault_uid):
    """used to remove vault access of a vault
    """
    try:
        logger.debug(f'Enter {__name__} module, remove_vault_access method')

        organization_id = request.query_params.get('organization_id')

        deleted_vault_access = user_access_service.remove_vault_access(
            organization_id, employee_uid, vault_uid
        )

        logger.debug(f'Exit {__name__} module, remove_vault_access method')
        return Response(deleted_vault_access)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, remove_vault_access method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def decrypt_item(request: HttpRequest, employee_uid, vault_uid, component_uid,
                 item_uid):
    logger.debug(f'Enter {__name__} module, decrypt_item method')

    try:
        organization_id = request.query_params.get('organization_id')

        decrypted_item = item_service.decrypt_item(
            request.data, organization_id, employee_uid, vault_uid,
            component_uid, item_uid)
        logger.debug(f'Exit {__name__} module, decrypt_item method')
        return Response(decrypted_item)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, decrypt_item method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['POST', 'GET'])
def decrypt(request: HttpRequest):
    """used to render the decrypted value
    """
    if request.method == 'GET':
        return render(request, 'decrypt.html')
    elif request.method == 'POST':
        token = request.data.get('token')
        secret_key = request.data.get('secret_key')

        if not token or not secret_key:
            return render(request, 'decrypt.html',
                          {'error': 'Enter both token and secret key'})

        decrypted_value = encryptor.decrypt(token, secret_key)

        if decrypted_value is None:
            return render(request, 'decrypt.html',
                          {'error': 'Decryption failure. '
                                    'Enter valid details.'})

        return render(request, 'decrypt.html',
                      {'decrypted_value': decrypted_value})
