"""This module is used to call operations on
vaults. components, item and usr accesses
"""
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from credential.models import Project
from credential.serializer import VaultSerializer, ProjectSerializer
from credential.serializer import ComponentSerializer

from credential.service import component_service
from credential.service import user_access_service
from credential.service import vault_service

from credential.utils.api_exceptions import CustomApiException


@api_view(['POST'])
def create_vault(request: HttpRequest, project_id):
    vault = vault_service.create_vault(project_id, request.data)
    return Response(vault)


@api_view(['GET', 'PUT', 'PATCH'])
def do_vault(request: HttpRequest, project_id, vault_id):
    if request.method == 'GET':
        vault = vault_service.get_vault(project_id, vault_id, request.data)

        if vault is None:
            raise CustomApiException(400,
                                     'You don\' have access for this vault.'
                                     'Please check your credentials')

        serializer = VaultSerializer(vault)
        return Response(serializer.data)

    if request.method == 'PUT':
        vault = vault_service.update_vault(project_id, vault_id, request.data)
        return Response(vault)

    if request.method == 'PATCH':
        vault_active_status = vault_service \
            .change_active_status(vault_id, request.data)
        return Response(f'Active status changes to {vault_active_status}')


@api_view(['POST'])
def create_component(request: HttpRequest, project_id, vault_id):
    component = component_service.create_component(project_id, vault_id,
                                                   request.data)
    return Response(component)


@api_view(['GET', 'PUT', 'PATCH'])
def do_component(request: HttpRequest, project_id, vault_id, component_id):
    if request.method == 'GET':
        component = component_service.get_component(project_id, vault_id,
                                                    component_id, request.data)

        if component is None:
            raise CustomApiException(400, 'You don\' have access for '
                                          'this component.'
                                          'Please check your credentials')

        serializer = ComponentSerializer(component)
        return Response(serializer.data)

    if request.method == 'PUT':
        component = component_service.update_component(project_id, vault_id,
                                                       component_id,
                                                       request.data)
        return Response(component)

    if request.method == 'PATCH':
        component_active_status = component_service \
            .change_active_status(vault_id, component_id, request.data)
        return Response(f'Active status changes to {component_active_status}')


@api_view(['POST', 'PUT', 'PATCH'])
def do_vault_access(request: HttpRequest, project_id, vault_id):
    if request.method == 'POST':
        vault_access = user_access_service.create_vault_access(project_id,
                                                               vault_id,
                                                               request.data)
        return Response(vault_access)

    if request.method == 'PATCH':
        return user_access_service.remove_vault_access(project_id, vault_id,
                                                       request.data)


@api_view(['POST', 'PUT', 'PATCH'])
def do_component_access(request: HttpRequest, project_id, vault_id,
                        component_id):
    if request.method == 'POST':
        component_access = user_access_service.create_component_access(
            project_id, vault_id, component_id, request.data)
        return Response(component_access)

    if request.method == 'PATCH':
        return user_access_service.remove_component_access(project_id,
                                                           vault_id,
                                                           component_id,
                                                           request.data)


@api_view(['POST'])
def get(request):
    project = Project.objects.get(project_id=request.data.get('project_id'))
    return Response(ProjectSerializer(project).data)
