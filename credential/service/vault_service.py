"""This module is used to create, update and delete
vault for the project
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from credential.models import Vault
from credential.serializer import VaultSerializer

from credential.service import user_access_service
from credential.service import employee_service

from credential.utils.api_exceptions import CustomApiException


def create_vault(project_id, data):
    try:
        employee = employee_service \
            .is_organization_employee(data.get('email_address'))

        if employee is None:
            raise CustomApiException(404,
                                     'You are not belonging '
                                     'to the organization')

        # data['project'] = project_id

        vault_serializer = VaultSerializer(data=data)
        vault_serializer.is_valid(raise_exception=True)
        vault_serializer.save()

        return vault_serializer.data
    except (ValidationError, KeyError):
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        raise CustomApiException(404,
                                 'You are not belonging to the organization')


def get_vault(project_id, vault_id, data):
    try:
        email_address = data.get('email_address')

        vault = Vault.objects.get(vault_id=vault_id, active=True)

        vault_access = user_access_service.get_vault_access(vault_id,
                                                            email_address)

        if vault.email_address == email_address:
            return vault
        elif vault_access is not None:
            return vault
        elif vault.access_level == 'ORGANIZATION' \
                and employee_service.is_organization_employee(email_address) \
                is not None:
            return vault
        elif vault.access_level == 'PROJECT' \
                and employee_service \
                .is_project_employee(email_address, project_id) is not None:
            return vault
        else:
            return None
    except KeyError:
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        raise CustomApiException(500, 'No such vault exist')


def update_vault(project_id, vault_id, data):
    try:
        email_address = data.get('email_address')

        vault = Vault.objects.get(vault_id=vault_id,
                                  email_address=email_address)

        vault_serializer = VaultSerializer(vault, data=data, partial=True)
        vault_serializer.is_valid(raise_exception=True)
        vault_serializer.save()

        vault = vault_serializer.data
        vault.pop('components')

        return vault
    except (ValidationError, KeyError):
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        raise CustomApiException(404, 'No such vault exist')


def change_active_status(vault_id, data):
    try:
        email_address = data.get('email_address')
        active = data.get('active')

        vault = Vault.objects.get(vault_id=vault_id)

        if vault.email_address == email_address:
            vault.active = active
            vault.save()
            return active
        else:
            raise CustomApiException(400, 'You don\'t have access'
                                          'to change active status')
    except KeyError:
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        raise CustomApiException(404, 'No such vault exist')
