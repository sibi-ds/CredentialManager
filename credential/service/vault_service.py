"""This module is used to create, update and delete vault
"""
import logging

from credential.models import Vault

from credential.serializers import VaultSerializer

from rest_framework.exceptions import ValidationError

from employee.models import Employee
from credential.service import user_access_service
from organization.models import Organization

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_vault(organization_id, uid, data):
    """used to create vault in an organization
    """
    logger.info(f'Enter {__name__} module, {create_vault.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization,
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
    except Organization.DoesNotExist:
        logger.error('Vault creation failure. No such organization exist')
        logger.error(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


def get_vault(organization_id, uid, vault_id):
    """used to get vault from an organization
    """
    logger.info(f'Enter {__name__} module, {get_vault.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        vault = Vault.objects.get(
            vault_id=vault_id, active=True,
            organization=organization,
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization,
        )

        if user_access_service.has_vault_access(organization_id, employee,
                                                vault_id):
            vault_serializer = VaultSerializer(vault)
            logger.info(f'Exit {__name__} module, '
                        f'{get_vault.__name__} method')
            return vault_serializer.data
        else:
            logger.error(f'Exit {__name__} module, '
                         f'{get_vault.__name__} method')
            raise CustomApiException(400, 'You don\'t have access '
                                          'to this vault')
    except KeyError:
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Employee.DoesNotExist:
        logger.error(f'Employee for Employee UID : {uid} is not exist')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except CustomApiException as e:
        logger.error('Enter valid credentials')
        logger.error(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def update_vault(organization_id, uid, vault_id, data):
    """used to update vault details
    """
    logger.info(f'Enter {__name__} module, {update_vault.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        vault = Vault.objects.get(
            vault_id=vault_id,
            organization=organization
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization,
        )

        if user_access_service.can_update_vault(organization_id, employee,
                                                vault_id):
            data['updated_by'] = employee.employee_id
            vault_serializer = VaultSerializer(vault, data=data, partial=True)
            vault_serializer.is_valid(raise_exception=True)
            vault_serializer.save()

            vault = vault_serializer.data
            vault.pop('components')

            logger.debug('Vault details updated successfully')
            logger.debug(f'Exit {__name__} module, '
                         f'{update_vault.__name__} method')

            return vault
        else:
            logger.error('Vault update failure. '
                         'User don\'t have vault update access')
            logger.error(f'Exit {__name__} module, '
                         f'{update_vault.__name__} method')
            raise CustomApiException(400,
                                     'You don\'t have vault update access')
    except (ValidationError, KeyError):
        logger.error('Valid details not provided')
        logger.error(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error(f'vault for Employee UID : {uid} is not exist')
        logger.error(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
