"""This module is used to achieve vault and component
accesses for the employees in an organization
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response

from credential.models import ComponentAccess
from credential.models import VaultAccess

from credential.serializer import ComponentAccessSerializer
from credential.serializer import VaultAccessSerializer

from credential.service import employee_service

from credential.utils.api_exceptions import CustomApiException


def create_vault_access(project_id, vault_id, data):
    try:
        email_address = data.pop('email_address')

        vault_accesses = VaultAccess.objects \
            .filter(vault=vault_id,
                    employee=email_address,
                    active=True)

        if len(vault_accesses) > 0:
            raise CustomApiException(500, 'Access already given')

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
    except (KeyError, ValidationError):
        raise CustomApiException(500, 'Enter valid details')


def remove_vault_access(project_id, vault_id, data):
    try:
        employee_email_address = data.pop('email_address')

        vault_access = VaultAccess.objects.get(
            employee=employee_email_address,
            vault=vault_id
        )

        vault_access_serializer = VaultAccessSerializer(vault_access,
                                                        data=data,
                                                        partial=True)
        vault_access_serializer.is_valid(raise_exception=True)
        vault_access_serializer.save()

        return Response('The access for ' + employee_email_address
                        + ' is removed')
    except ObjectDoesNotExist:
        return Response('No such vault access exist')
    except (ValidationError, KeyError):
        return CustomApiException(500, 'Enter valid details')


def get_vault_access(vault_id, email_address):
    try:
        vault_access = VaultAccess.objects.get(vault=vault_id,
                                               employee=email_address,
                                               active=True)
        return vault_access
    except ObjectDoesNotExist:
        return None


def create_component_access(project_id, vault_id, component_id, data):
    try:
        email_address = data.pop('email_address')

        component_accesses = ComponentAccess.objects \
            .filter(component=component_id,
                    employee=email_address,
                    active=True)

        if len(component_accesses) > 0:
            raise CustomApiException(500, 'Access already given')

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
    except (ValidationError, KeyError):
        raise CustomApiException(500, 'Enter valid details')


def remove_component_access(project_id, vault_id, component_id, data):
    try:
        employee_email_address = data.get('email_address')

        component_access = ComponentAccess.objects.get(
            employee=employee_email_address,
            component=component_id
        )

        component_access_serializer = ComponentAccessSerializer(
            component_access, data=data, partial=True
        )

        component_access_serializer.is_valid(raise_exception=True)
        component_access_serializer.save()

        return Response('The access for ' + employee_email_address
                        + ' is removed')
    except ObjectDoesNotExist:
        return Response('No such component access exist')
    except (ValidationError, KeyError):
        raise CustomApiException(500, 'Enter valid details')


def get_component_access(component_id, email_address):
    try:
        component = ComponentAccess.objects.get(component_id=component_id,
                                                employee=email_address,
                                                active=True)
        return component
    except ObjectDoesNotExist:
        return None
