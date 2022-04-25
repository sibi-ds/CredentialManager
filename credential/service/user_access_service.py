"""This module is used to achieve vault and component
accesses for the employees in an organization
"""
import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from credential.models import Component
from credential.models import ComponentAccess
from credential.models import Vault
from credential.models import VaultAccess

from credential.serializers import ComponentAccessSerializer
from credential.serializers import VaultAccessSerializer

from credential.utils.api_exceptions import CustomApiException

from employee.service import employee_service


logger = logging.getLogger('credential-manager-logger')


def get_vault_access(vault_id, email):
    """used to get vault access for an employee
    """
    logger.info(f'Enter {__name__} module, {get_vault_access.__name__} method')

    try:
        vault_access = VaultAccess.objects.get(vault=vault_id,
                                               employee=email,
                                               active=True)
        logger.info(f'Exit {__name__} module, '
                    f'{get_vault_access.__name__} method')
        return vault_access
    except ObjectDoesNotExist:
        logger.error('Vault Access for the given credentials does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_vault_access.__name__} method')
        return None


def create_vault_access(vault_id, data):
    """used to create vault access for an employee
    """
    logger.info(f'Enter {__name__} module, '
                f'{create_vault_access.__name__} method')

    try:
        email = data.pop('email')

        vault = Vault.objects.get(vault_id=vault_id, active=True)

        employee = employee_service.is_organization_employee(email)

        if employee is None:
            logger.error('Employee not belongs to the organization')
            logger.error(f'Exit {__name__} module, '
                         f'{create_vault_access.__name__} method')
            raise CustomApiException(500, 'This user is not belong '
                                          'to the organization')

        data['vault'] = vault_id
        data['employee'] = email

        vault_access = get_vault_access(vault_id, email)

        if vault_access is not None:
            logger.error('Vault access already given')
            logger.error(f'Exit {__name__} module, '
                         f'{create_vault_access.__name__} method')
            raise CustomApiException(500, 'Vault access already given '
                                          'for the employee')

        vault_access_serializer = VaultAccessSerializer(data=data)
        vault_access_serializer.is_valid(raise_exception=True)
        vault_access_serializer.save()

        logger.info(f'Exit {__name__} module, '
                    f'{create_vault_access.__name__} method')

        return vault_access_serializer.data
    except (KeyError, ValidationError):
        logger.error('The entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such vault exist')


def remove_vault_access(vault_id, data):
    """used to remove vault access of the employee
    """
    logger.info(f'Enter {__name__} module, '
                f'{remove_vault_access.__name__} method')

    try:
        email = data.pop('email')

        vault_access = VaultAccess.objects.get(
            employee=email,
            vault=vault_id,
            active=True
        )

        vault_access_serializer = VaultAccessSerializer(vault_access,
                                                        data=data,
                                                        partial=True)
        vault_access_serializer.is_valid(raise_exception=True)
        vault_access_serializer.save()

        logger.info('Vault access status changed successfully')
        logger.info(f'Exit {__name__} module, '
                    f'{remove_vault_access.__name__} method')

        return Response('The access for ' + email
                        + ' is changed successfully')
    except ObjectDoesNotExist:
        logger.error('The vault access does not exist '
                     'for the given credentials')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_vault_access.__name__} method')
        return Response('No such vault access exist')
    except (ValidationError, KeyError):
        logger.error('The given email address is not belong '
                     'to the organization')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_vault_access.__name__} method')
        return CustomApiException(500, 'Enter valid details')


def get_component_access(component_id, email):
    """used to get component access of an employee
    """
    logger.info(f'Enter {__name__} module, '
                f'{get_component_access.__name__} method')

    try:
        component = ComponentAccess.objects.get(component_id=component_id,
                                                employee=email,
                                                active=True)

        logger.info(f'Exit {__name__} module, '
                    f'{get_component_access.__name__} method')

        return component
    except ObjectDoesNotExist:
        logger.error('The given email address is not given access')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component_access.__name__} method')
        return None


def create_component_access(vault_id, component_id, data):
    """used to create component access of an employee
    """
    logger.info(f'Enter {__name__} module, '
                f'{create_component_access.__name__} method')

    try:
        email = data.pop('email')

        vault = Vault.objects.get(vault_id=vault_id, active=True)

        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id,
                                          active=True)

        employee = employee_service.is_organization_employee(email)

        if employee is None:
            logger.error('The given email address is not belong '
                         'to the organization')
            logger.error(f'Exit {__name__} module, '
                         f'{create_component_access.__name__} method')
            raise CustomApiException(400, 'This user is not belong '
                                          'to the organization')

        data['employee'] = email
        data['component'] = component_id

        component_access = get_component_access(component_id, email)

        if component_access is not None:
            logger.error('Component access already given')
            logger.error(f'Exit {__name__} module, '
                         f'{create_component_access.__name__} method')
            raise CustomApiException(400, 'Component access already given'
                                          'for the employee')

        component_access_serializer = ComponentAccessSerializer(data=data)
        component_access_serializer.is_valid(raise_exception=True)
        component_access_serializer.save()

        logger.info(f'Exit {__name__} module, '
                    f'{create_component_access.__name__} method')

        return component_access_serializer.data
    except Vault.DoesNotExist:
        logger.error('The entered credentials can\'t create component access')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component_access.__name__} method')
        raise CustomApiException(404, 'You don\'t have access '
                                      'to create component access')
    except Component.DoesNotExist:
        logger.error(f'Component for Component ID : {component_id}'
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component_access.__name__} method')
        raise CustomApiException(404, 'Component does not exist')
    except (ValidationError, KeyError):
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component_access.__name__} method')
        raise CustomApiException(500, 'Enter valid details')


def remove_component_access(component_id, data):
    """used to remove component access of the employee
    """
    logger.info(f'Enter {__name__} module, '
                f'{remove_component_access.__name__} method')

    try:
        email = data.get('email')

        component_access = ComponentAccess.objects.get(
            employee=email,
            component=component_id,
            active=True
        )

        component_access_serializer = ComponentAccessSerializer(
            component_access, data=data, partial=True
        )

        component_access_serializer.is_valid(raise_exception=True)
        component_access_serializer.save()

        logger.info('The vault access status changed successfully')
        logger.info(f'Exit {__name__} module, '
                    f'{remove_component_access.__name__} method')

        return Response('The access for ' + email
                        + ' is changed successfully')
    except ObjectDoesNotExist:
        logger.error('No component access was provided for the given details')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_component_access.__name__} method')
        return Response('No such component access exist')
    except (ValidationError, KeyError):
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_component_access.__name__} method')
        raise CustomApiException(500, 'Enter valid details')
