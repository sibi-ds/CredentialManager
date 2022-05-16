""""""
import logging

from credential.models import Vault, Component, Item
from credential.service import user_access_service

from employee.models import Employee

from organization.models import Organization

from utils.api_exceptions import CustomApiException
from utils.encryption_decryption import decrypt


logger = logging.getLogger('credential-manager-logger')


def decrypt_item(data, organization_id, employee_uid, vault_uid,
                 component_uid, item_uid):
    """used to get decrypted value
    """
    logger.debug(f'Enter {__name__} module, {get_item.__name__} method')

    try:
        value = data.get('value', None)
        salt = data.get('salt', None)

        item = get_item(data, organization_id, employee_uid, vault_uid,
                        component_uid, item_uid)

        if value is None or salt is None:
            value = item.value
            salt = bytes(item.salt, 'utf-8')
        else:
            salt = bytes(salt, 'utf-8')

        decrypted_value = decrypt(value, salt)

        if decrypted_value is None:
            raise CustomApiException(400, 'Decryption Failure')

        return {'key': item.key, 'value': decrypted_value}
    except CustomApiException as e:
        logger.error('Decryption failure')
        logger.error(f'Exit {__name__} module, {get_item.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def get_item(data, organization_id, employee_uid, vault_uid, component_uid,
             item_uid):
    """used to get item
    """
    logger.debug(f'Enter {__name__} module, {get_item.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        vault = Vault.objects.get(
            vault_uid=vault_uid, active=True,
            organization=organization
        )

        employee = Employee.objects.get(
            employee_uid=employee_uid, active=True,
            organization=organization,
        )

        component = Component.objects.get(
            component_uid=component_uid,
            vault=vault, vault__active=True,
            organization=organization
        )

        item = Item.objects.get(
            item_uid=item_uid, active=True,
            component=component, component__active=True,
            organization=organization
        )

        if vault.created_by.employee_id == employee.employee_id \
                or user_access_service.has_vault_access(organization_id,
                                                        employee,
                                                        vault.vault_id):
            logger.debug(f'Exit {__name__} module, '
                         f'{get_item.__name__} method')
            return item
        else:
            logger.error(f'Exit {__name__} module, '
                         f'{get_item.__name__} method')
            raise CustomApiException(400, 'You don\'t have access '
                                          'to this vault')
    except KeyError:
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{get_item.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error(f'Organization with Organization ID: '
                     f'{organization_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_item.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error(f'vault for Employee UID : {employee_uid} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_item.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault UID : {vault_uid} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_item.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Component.DoesNotExist:
        logger.error(f'Component for Component UID : {component_uid} '
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_item.__name__} method')
        raise CustomApiException(404, 'No such component exist')
    except Item.DoesNotExist:
        logger.error(f'Item for Item UID : {item_uid} '
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_item.__name__} method')
        raise CustomApiException(404, 'No such item exist')
