"""This module is used to create, update and delete
components of a vault
"""
import logging

from rest_framework.exceptions import ValidationError

from credential.models import Component
from credential.models import Vault

from credential.serializers import ComponentSerializer, \
    ComponentResponseSerializer
from credential.service import user_access_service

from employee.models import Employee

from organization.models import Organization

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_component(organization_id, uid, vault_id, data):
    """used to create component for a vault
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_component.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        vault = Vault.objects.get(
            vault_id=vault_id, active=True,
            organization=organization,
            organization__active=True,
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization__organization_id=organization_id,
            organization__active=True
        )

        if user_access_service.can_update_vault(organization_id, employee,
                                                vault_id):
            data['vault'] = vault.vault_id
            data['organization'] = organization.organization_id
            data['created_by'] = employee.employee_id

            component_serializer = ComponentSerializer(data=data, partial=True)

            component_serializer.is_valid(raise_exception=True)
            component_serializer.save()

            logger.debug('Component created successfully')
            logger.debug(f'Exit {__name__} module, '
                         f'{create_component.__name__} method')

            return component_serializer.data
        else:
            logger.error('Component creation failure. '
                         'User don\'t have component creation access')
            logger.error(f'Exit {__name__} module, '
                         f'{create_component.__name__} method')
            raise CustomApiException(400, 'You don\'t have component '
                                          'creation access')
    except ValidationError:
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error(f'Component creation failure. '
                     f'Organization with Organization ID: '
                     f'{organization_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Vault.DoesNotExist:
        logger.error(f'Component creation failure. '
                     f'Vault with Vault ID:  {vault_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(400, 'No such vault exist')
    except Employee.DoesNotExist:
        logger.error('Component creation failure. No such employee exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(404, 'No such employee exist')


def get_component(organization_id, uid, vault_id, component_id, data):
    """used to get component and its items from a vault
    """
    logger.debug(f'Enter {__name__} module, {get_component.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        vault = Vault.objects.get(
            vault_id=vault_id, active=True,
            organization=organization
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization,
        )

        component = Component.objects.get(
            component_id=component_id,
            vault=vault, vault__active=True,
            organization=organization
        )

        if user_access_service.has_vault_access(organization_id, employee,
                                                vault_id):
            component_serializer = ComponentResponseSerializer(component)
            logger.debug(f'Exit {__name__} module, '
                         f'{get_component.__name__} method')
            return component_serializer.data
        else:
            logger.error(f'Exit {__name__} module, '
                         f'{get_component.__name__} method')
            raise CustomApiException(400, 'You don\'t have access '
                                          'to this vault')
    except KeyError:
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error(f'Organization with Organization ID: '
                     f'{organization_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error(f'vault for Employee UID : {uid} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Component.DoesNotExist:
        logger.error(f'Component for Component ID : {component_id} '
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component.__name__} method')
        raise CustomApiException(404, 'No such component exist')


def update_component(organization_id, uid, vault_id, component_id, data):
    """used to update component details and items
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{update_component.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        vault = Vault.objects.get(
            vault_id=vault_id, active=True,
            organization=organization
        )

        employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization,
        )

        component = Component.objects.get(
            component_id=component_id,
            vault=vault, vault__active=True,
            organization=organization,
        )

        if user_access_service.can_update_vault(organization_id, employee,
                                                vault_id):
            data['updated_by'] = employee.employee_id
            component_serializer = ComponentSerializer(component, data=data,
                                                       partial=True)
            component_serializer.is_valid(raise_exception=True)
            component_serializer.save()

            component = component_serializer.data

            logger.debug('Component details updated successfully')
            logger.debug(f'Exit {__name__} module, '
                         f'{update_component.__name__} method')

            return component
        else:
            logger.error('Component update failure.')
            logger.error(f'Exit {__name__} module, '
                         f'{update_component.__name__} method')
            raise CustomApiException(400,
                                     'You don\'t have component update access')
    except (ValidationError, KeyError):
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error('No such vault exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Component.DoesNotExist:
        logger.error(f'Component for Component ID : {component_id} '
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(404, 'No such component exist')
    except Employee.DoesNotExist:
        logger.error(f'vault for Employee UID : {uid} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
