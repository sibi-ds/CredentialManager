"""This module is used to create, update and delete
components for the vault
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from credential.models import Component
from credential.models import Vault

from credential.serializer import ComponentSerializer

from credential.service import employee_service
from credential.service import user_access_service

from rest_framework.response import Response

from credential.utils.api_exceptions import CustomApiException


def create_component(project_id, vault_id, data):
    try:
        data['vault'] = vault_id

        component_serializer = ComponentSerializer(data=data)
        component_serializer.is_valid(raise_exception=True)
        print(component_serializer.errors)
        print(component_serializer)
        component_serializer.save()

        return component_serializer.data
    except ValidationError:
        raise CustomApiException(500, 'Enter valid details')


def get_component(project_id, vault_id, component_id, data):
    try:
        email_address = data.get('email_address')

        vault = Vault.objects.get(vault_id=vault_id)

        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id)

        component_access = user_access_service \
            .get_component_access(component_id, email_address)

        vault_access = user_access_service \
            .get_vault_access(vault_id, email_address)

        if vault.email_address == email_address:
            return component
        elif vault_access is not None \
                and vault_access.email_address == email_address:
            return component
        elif component_access is not None \
                and component_access.email_adddress == email_address:
            return component
        elif (vault.access_level == 'ORGANIZATION'
                or component.access_level == 'ORGANIZATION') \
                and employee_service \
                .is_organization_employee(email_address) is not None:
            return component
        elif (vault.access_level == 'PROJECT'
                or component.access_level == 'PROJECT') \
                and employee_service \
                .is_project_employee(email_address, project_id) is not None:
            return component
        else:
            return None
    except ObjectDoesNotExist:
        raise CustomApiException(400, 'No such component exist')


def update_component(project_id, vault_id, component_id, data):
    try:
        component = Component.objects.get(component_id=component_id)
        component_serializer = ComponentSerializer(instance=component, data=data)

        component_serializer.is_valid(raise_exception=True)
        component_serializer.save()

        return component_serializer.data
    except ValidationError:
        raise CustomApiException(500, 'Enter valid details')


def serialize(data):
    serializer = ComponentSerializer(data)
    return Response(serializer.data)
