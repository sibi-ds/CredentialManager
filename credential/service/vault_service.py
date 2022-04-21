"""This module is used to create, update and delete
vault for the project
"""
import logging

from django.core.exceptions import ObjectDoesNotExist

from credential.models import Vault

from credential.serializers import VaultSerializer

from rest_framework.exceptions import ValidationError

from credential.service import employee_service
from credential.service import user_access_service

from credential.utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_vault(data):
    logger.info(f'Enter {__name__} module, {create_vault.__name__} method')

    try:
        employee = employee_service \
            .is_organization_employee(data.get('email'))

        if employee is None:
            logger.error('The given email address is not belong '
                         'to the organization')
            logger.info(
                f'Exit {__name__} module, {create_vault.__name__} method')
            raise CustomApiException(404,
                                     'You are not belonging '
                                     'to the organization')

        vault_serializer = VaultSerializer(data=data)
        vault_serializer.is_valid(raise_exception=True)
        vault_serializer.save()

        logger.info('Vault creation successful')
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        return vault_serializer.data
    except (ValidationError, KeyError):
        logger.error('Vault creation failure')
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        logger.error('Vault creation failure')
        logger.info(f'Exit {__name__} module, {create_vault.__name__} method')
        raise CustomApiException(404,
                                 'You are not belonging to the organization')


def get_vault(vault_id, data):
    logger.info(f'Enter {__name__} module, {get_vault.__name__} method')

    try:
        email = data.get('email')

        vault = Vault.objects.get(vault_id=vault_id, active=True)

        vault_access = user_access_service.get_vault_access(vault_id, email)

        response_vault = None

        if vault.email == email:
            response_vault = vault
        elif vault_access is not None:
            response_vault = vault
        elif vault.access_level == 'ORGANIZATION' \
                and employee_service.is_organization_employee(email) \
                is not None:
            response_vault = vault
        elif vault.project is not None \
                and vault.access_level == 'PROJECT' \
                and employee_service \
                .is_project_employee(email, vault.project) is not None:
            response_vault = vault

        if response_vault is None:
            raise CustomApiException(400, 'You don\'t have access '
                                          'for this vault')

        vault_serializer = VaultSerializer(response_vault)

        logger.info(f'Exit {__name__} module, {get_vault.__name__} method')

        return vault_serializer.data
    except KeyError:
        logger.error('Enter valid details')
        logger.info(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        logger.error(f'vault for Vault ID : {vault_id} is not exist')
        logger.info(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except CustomApiException as e:
        logger.error('The given credentials has no access for this vault')
        logger.info(f'Exit {__name__} module, {get_vault.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def update_vault(vault_id, data):
    logger.info(f'Enter {__name__} module, {update_vault.__name__} method')

    try:
        email = data.get('email')

        vault = Vault.objects.get(vault_id=vault_id,
                                  email=email)

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
        logger.info(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.info(f'Exit {__name__} module, {update_vault.__name__} method')
        raise CustomApiException(404, 'No such vault exist')


def change_active_status(vault_id, data):
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
        logger.info(f'Exit {__name__} module, '
                    f'{change_active_status.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except ObjectDoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.info(f'Exit {__name__} module, '
                    f'{change_active_status.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except CustomApiException as e:
        logger.error('Entered credentials don\'t have access '
                     'to change the vault active status')
        logger.info(f'Exit {__name__} module, '
                    f'{change_active_status.__name__} method')
        raise CustomApiException(e.status_code, e.detail)
