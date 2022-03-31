from django.core.exceptions import ObjectDoesNotExist

from django.db import DatabaseError
from django.db import transaction

from rest_framework.response import Response

from credential.models import Component, Employee
from credential.models import ComponentAccess
from credential.models import Item
from credential.models import Vault

from credential.serializer import ComponentDeSerializer
from credential.serializer import ComponentSerializer
from credential.service import user_access_service, employee_service


def create_component(project_id, vault_id, data):
    try:
        data['vault'] = vault_id
        serializer = ComponentDeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return None
    except Exception as ex:
        print(ex)
        return None


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
        return None


def update_component(project_id, vault_id, component_id, data):
    component = Component.objects.get(component_id=component_id)
    serializer = ComponentDeSerializer(instance=component, data=data)

    if serializer.is_valid():
        component = serializer.save()

    return component


def serialize(data):
    serializer = ComponentSerializer(data)
    return Response(serializer.data)
