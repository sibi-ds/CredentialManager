from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from credential.models import Employee, VaultAccess
from credential.models import ComponentAccess
from credential.models import Vault

from credential.serializer import ComponentAccessSerializer


def create_vault_access(project_id, vault_id, data):
    try:
        employee_email_address = data.get('email_address')
        employee = Employee.objects.get(projects__project_id=project_id,
                                        email_address=employee_email_address)

        vault_access = VaultAccess.objects.create(
            employee_id=employee_email_address,
            vault_id=vault_id
        )

        return vault_access
    except ObjectDoesNotExist:
        return None


def remove_vault_access(project_id, vault_id, data):
    pass


def get_vault_access(vault_id, email_address):
    try:
        vault_access = VaultAccess.objects.get(vault_id=vault_id,
                                               employee_id=email_address)
        return vault_access
    except ObjectDoesNotExist:
        return None


def create_component_access(project_id, vault_id, component_id, data):
    try:
        employee_email_address = data.get('email_address')
        employee = Employee.objects.get(email_address=employee_email_address)

        component_access = ComponentAccess.objects.create(
            employee_id=employee_email_address,
            component_id=component_id
        )

        return component_access
    except ObjectDoesNotExist:
        return None


def remove_component_access(project_id, vault_id, component_id, data):
    employee_email_address = data.get('email_address')
    user_access = ComponentAccess.objects.get(
        employee_id=employee_email_address,
        component_id=component_id
    )
    user_access.delete()
    return Response('The access for ' + employee_email_address + 'is removed')


def get_component_access(component_id, email_address):
    try:
        component = ComponentAccess.objects.get(component_id=component_id,
                                                employee_id=email_address)
        return component
    except ObjectDoesNotExist:
        return None


def serialize(data):
    serializer = ComponentAccessSerializer(data)
    return Response(serializer.data)
