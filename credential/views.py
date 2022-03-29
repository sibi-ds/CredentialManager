"""This module is used to
do the operations on credentials
"""
from django.http import HttpRequest
from django.http import HttpResponse

from django.db import DatabaseError
from django.db import IntegrityError
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response

from credential.serializer import VaultSerializer
from credential.serializer import ComponentSerializer
from credential.serializer import ItemSerializer
from credential.serializer import UserAccessSerializer

from credential.models import Vault
from credential.models import Component
from credential.models import UserAccess

from credential.service import component_service
from credential.service import user_access_service
from credential.service import vault_service


@api_view(['POST'])
def create_vault(request: HttpRequest, project_id):
    return vault_service.create_vault(project_id, request.data)


@api_view(['GET', 'PUT', 'DELETE'])
def do_vault(request: HttpRequest, project_id, vault_id):

    if request.method == 'GET':
        return vault_service.get_vault(project_id, vault_id, request.data)

    if request.method == 'PUT':
        return vault_service.update_vault(project_id, vault_id, request.data)


@api_view(['POST'])
def create_component(request: HttpRequest, project_id, vault_id):
    return component_service.create_component(project_id,
                                              vault_id,
                                              request.data)


@api_view(['GET', 'PUT', 'DELETE'])
def do_component(request: HttpRequest, project_id, vault_id, component_id):

    if request.method == 'GET':
        return component_service.get_component(project_id, vault_id,
                                               component_id, request.data)

    if request.method == 'PUT':
        return component_service.update_component(project_id, vault_id,
                                                  component_id, request.data)


@api_view(['POST', 'PUT', 'DELETE'])
def do_access(request: HttpRequest, project_id, vault_id, component_id):
    if request.method == 'POST':
        return user_access_service.create_user_access(project_id,
                                                      vault_id,
                                                      component_id,
                                                      request.data)

    if request.method == 'DELETE':
        return user_access_service.remove_user_access(project_id,
                                                      vault_id,
                                                      component_id,
                                                      request.data)
