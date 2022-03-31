"""This module is used to
do the operations on credentials
"""
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from credential.serializer import VaultSerializer, ProjectSerializer, \
    VaultAccessSerializer, EmployeeSerializer
from credential.serializer import ComponentSerializer
from credential.serializer import ComponentAccessSerializer

from credential.models import Vault, Employee
from credential.models import Project
from credential.models import Component
from credential.models import ComponentAccess

from credential.service import component_service
from credential.service import user_access_service
from credential.service import vault_service


@api_view(['POST'])
def create_vault(request: HttpRequest, project_id):
    vault = vault_service.create_vault(project_id, request.data)
    serializer = VaultSerializer(vault)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def do_vault(request: HttpRequest, project_id, vault_id):

    if request.method == 'GET':
        vault = vault_service.get_vault(project_id, vault_id, request.data)

        if vault is None:
            return Response('No vault found')

        serializer = VaultSerializer(vault)
        return Response(serializer.data)

    if request.method == 'PUT':
        vault = vault_service.update_vault(project_id, vault_id, request.data)
        serializer = VaultSerializer(vault)
        return Response(serializer.data)


@api_view(['POST'])
def create_component(request: HttpRequest, project_id, vault_id):
    component = component_service.create_component(project_id,
                                                   vault_id,
                                                   request.data)

    return component


@api_view(['GET', 'PUT', 'DELETE'])
def do_component(request: HttpRequest, project_id, vault_id, component_id):

    if request.method == 'GET':
        component = component_service.get_component(project_id, vault_id,
                                                    component_id,
                                                    request.data)
        serializer = ComponentSerializer(component)
        return Response(serializer.data)

    if request.method == 'PUT':
        component = component_service.update_component(project_id, vault_id,
                                                       component_id,
                                                       request.data)
        serializer = ComponentSerializer(component)
        return Response(serializer.data)


@api_view(['POST', 'PUT', 'DELETE'])
def do_vault_access(request: HttpRequest, project_id, vault_id):
    if request.method == 'POST':
        vault_access = user_access_service.create_vault_access(project_id,
                                                               vault_id,
                                                               request.data)

        if vault_access is None:
            return Response('vault access creation failure for {}'
                            .request.data.get('email_address'))

        serializer = VaultAccessSerializer(vault_access)
        return Response(serializer.data)

    if request.method == 'DELETE':
        return user_access_service.remove_vault_access(project_id,
                                                       vault_id,
                                                       request.data)


@api_view(['POST', 'PUT', 'DELETE'])
def do_component_access(request: HttpRequest, project_id, vault_id, component_id):
    if request.method == 'POST':
        component_access = user_access_service.create_component_access(project_id,
                                                                  vault_id,
                                                                  component_id,
                                                                  request.data)
        serializer = ComponentAccessSerializer(component_access)
        return Response(serializer.data)

    if request.method == 'DELETE':
        return user_access_service.remove_component_access(project_id,
                                                           vault_id,
                                                           component_id,
                                                           request.data)


@api_view(['POST'])
def get(request, project_id):
    # projects = Project.objects.get(project_id=project_id)
    # serializer = ProjectSerializer(projects)
    # return Response(serializer.data)

    email_address = request.data.get('email_address')
    print(email_address, request.data)
    employee = Employee.objects.get(email_address=email_address,
                                    projects__project_id=project_id)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)
