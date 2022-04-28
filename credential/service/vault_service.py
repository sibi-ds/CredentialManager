"""This module is used to create, update and delete vault
"""
import logging

from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher, \
    check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from credential.models import Vault, VaultAccess

from credential.serializers import VaultSerializer

from rest_framework.exceptions import ValidationError

from employee.models import Employee
from employee.service import employee_service
from credential.service import user_access_service
from organization.models import Organization
from project.models import Project

from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


@transaction.atomic
def create_vault(organization_id, uid, data):
    """used to create vault for a specific employee of the organization
    where project mapping is optional
    """
    logger.info(f'Enter {__name__} module, {create_vault.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization__organization_id=organization_id,
            organization__active=True
        )

        data['created_by'] = employee.employee_id
        data['organization'] = organization_id

        vault_serializer = VaultSerializer(data=data)
        vault_serializer.is_valid(raise_exception=True)
        vault_serializer.save()

        logger.info('Vault creation successful')
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        return vault_serializer.data
    except (ValidationError, KeyError):
        logger.error('Vault creation failure. Enter valid details')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Employee.DoesNotExist:
        logger.error('Vault creation failure. No such employee exist')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(404, 'No such employee exist')


def get_vault(organization_id, uid, vault_id, data):
    """used to get vault of a specific user
    """
    logger.info(f'Enter {__name__} module, {get_vault.__name__} method')

    try:
        vault = Vault.objects.get(
            vault_id=vault_id,
            organization__organization_id=organization_id,
            organization__active=True,
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization__organization_id=organization_id,
            organization__active=True
        )

        response_vault = None

        if user_access_service.get_admin_vault_access(
                organization_id, employee.employee_id, vault_id) is not None:
            response_vault = vault
        elif len(user_access_service.get_organization_vault_accesses(
                organization_id, vault_id)) > 0:
            response_vault = vault
        elif len(user_access_service.get_project_vault_accesses(
                organization_id, vault_id, employee.projects.all())) > 0:
            response_vault = vault
        elif len(user_access_service.get_individual_vault_accesses(
                organization_id, employee.employee_id, vault_id)) > 0:
            response_vault = vault

        if response_vault is None:
            raise CustomApiException(400, 'You don\'t have access '
                                          'for this vault')

        vault_serializer = VaultSerializer(response_vault)

        logger.info(f'Exit {__name__} module, {get_vault.__name__} method')

        return vault_serializer.data
    except KeyError:
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Employee.DoesNotExist:
        logger.error(f'vault for Employee UID : {uid} is not exist')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except CustomApiException as e:
        logger.error('Enter valid credentials')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def update_vault(organization_id, vault_id, data):
    """used to update vault details
    """
    logger.info(f'Enter {__name__} module, {update_vault.__name__} method')

    try:
        email = data.pop('employee')
        password = data.pop('password')

        vault = Vault.objects.get(
            vault_id=vault_id,
            organization__organization_id=organization_id
        )

        if not is_vault_owner(vault, email, password):
            logger.error(f'Exit {__name__} module, '
                         f'{update_vault.__name__} method')
            raise CustomApiException(400, 'Enter valid details')

        vault_serializer = VaultSerializer(vault, data=data, partial=True)
        vault_serializer.is_valid(raise_exception=True)
        vault_serializer.save()

        vault = vault_serializer.data
        vault.pop('components')

        logger.info('Vault details updated successfully')
        logger.info(f'Exit {__name__} module, {update_vault.__name__} method')

        return vault
    except (ValidationError, KeyError):
        logger.error('Valid details not provided')
        logger.error(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
