from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response

from credential.models import ComponentAccess
from credential.models import Employee
from credential.models import VaultAccess

from credential.serializer import ComponentAccessSerializer
from credential.serializer import VaultAccessSerializer

from credential.service import employee_service

from credential.utils.api_exceptions import CustomApiException


def create_vault_access(project_id, vault_id, data):
    try:
        email_address = data.pop('email_address')
        employee = employee_service.is_organization_employee(email_address)

        if employee is None:
            raise CustomApiException(500, 'This user is not belong '
                                          'to the organization')

        data['vault'] = vault_id
        data['employee'] = email_address

        vault_access_serializer = VaultAccessSerializer(data=data)
        vault_access_serializer.is_valid(raise_exception=True)
        vault_access_serializer.save()

        return vault_access_serializer.data
    except ValidationError:
        raise CustomApiException(500, 'Access already given')
    except KeyError:
        raise CustomApiException(500, 'Enter valid details')


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
        email_address = data.pop('email_address')
        employee = employee_service.is_organization_employee(email_address)

        if employee is None:
            raise CustomApiException(500, 'This user is not belong '
                                          'to the organization')

        data['employee'] = email_address
        data['component'] = component_id

        component_access_serializer = ComponentAccessSerializer(data=data)
        component_access_serializer.is_valid(raise_exception=True)
        component_access_serializer.save()

        return component_access_serializer.data
    except ValidationError:
        raise CustomApiException(500, 'Access already given')
    except KeyError:
        raise CustomApiException(500, 'Enter valid details')


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
