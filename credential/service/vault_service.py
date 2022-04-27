"""This module is used to create, update and delete vault
"""
import logging

from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher, \
    check_password
from django.core.exceptions import ObjectDoesNotExist

from credential.models import Vault, AccessLevel

from credential.serializers import VaultSerializer

from rest_framework.exceptions import ValidationError

from employee.models import Employee
from employee.service import employee_service
from credential.service import user_access_service
from organization.models import Organization
from project.models import Project

from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


def create_vault(organization_id, data):
    """used to create vault for a specific employee of the organization
    where project mapping is optional
    """
    logger.info(f'Enter {__name__} module, {create_vault.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        email = data.get('employee')
        access_level = data.get('access_level')

        employee = Employee.objects.get(email=email, active=True)
        access_level = AccessLevel.objects.get(
            access_level=access_level, active=True
        )

        data['employee'] = employee.employee_id
        data['organization'] = organization.organization_id
        data['access_level'] = access_level.access_level_id

        vault_serializer = VaultSerializer(data=data)
        vault_serializer.is_valid(raise_exception=False)
        print(vault_serializer.errors)
        vault_serializer.save()

        logger.info('Vault creation successful')
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        return vault_serializer.data
    except (ValidationError, KeyError):
        logger.error('Vault creation failure. Enter valid details')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Vault creation failure. No such organization exist')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error('Vault creation failure. No such employee exist')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except AccessLevel.DoesNotExist:
        logger.error('Vault creation failure. No such access level exist')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(404, 'No such access level exist')


def get_vault(organization_id, vault_id, data):
    """used to get vault of a specific user
    """
    logger.info(f'Enter {__name__} module, {get_vault.__name__} method')

    try:
        email = data.get('email')
        password = data.get('password')

        vault = Vault.objects.get(
            vault_id=vault_id,
            organization__organization_id=organization_id,
            organization__active=True,
        )

        response_vault = None

        if is_vault_owner(vault, email, password):
            response_vault = vault
        elif vault.access_level.access_level == 'ORGANIZATION' \
                and employee_service \
                .is_organization_employee(organization_id, email) \
                is not None:
            response_vault = vault
        elif vault.access_level.access_level == 'PROJECT' \
                and vault.project is not None \
                and employee_service \
                .is_project_employee(organization_id,
                                     vault.project.project_id, email) \
                is not None:
            response_vault = vault
        elif user_access_service.get_vault_access(vault_id, email) is not None:
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


def change_active_status(vault_id, data):
    """used to change active status of a vault
    """
    logger.info(f'Enter {__name__} module, '
                f'{change_active_status.__name__} method')

    try:
        email_address = data.get('email_address')
        active = data.get('active')

        vault = Vault.objects.get(vault_id=vault_id)

        if vault.email_address == email_address:
            vault.active = active
            vault.save()
            return active
        else:
            raise CustomApiException(400, 'You don\'t have access '
                                          'to change vault active status')
    except KeyError:
        logger.error('Valid details not provided')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except CustomApiException as e:
        logger.error('Entered credentials don\'t have access '
                     'to change the vault active status')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def is_vault_owner(vault, email, password):
    logger.info(f'Enter {__name__} module, '
                f'{is_vault_owner.__name__} method')

    if vault.employee.email == email \
            and check_password(password, vault.password):
        logger.info('The given credentials are '
                    'matching the vault credentials')
        logger.info(f'Exit {__name__} module, '
                    f'{is_vault_owner.__name__} method')

        return True
    else:
        logger.info('The given credentials are '
                    'not matching the vault credentials')
        logger.info(f'Exit {__name__} module, '
                    f'{is_vault_owner.__name__} method')

        return False
