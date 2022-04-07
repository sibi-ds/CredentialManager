"""This module is used to achieve vault and component
accesses for the employees in an organization
"""
import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response

from credential.models import ComponentAccess, Vault, Component
from credential.models import VaultAccess

from credential.serializer import ComponentAccessSerializer
from credential.serializer import VaultAccessSerializer

from credential.service import employee_service

from credential.utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_vault_access(vault_id, data):
    logger.info(f'Enter {__name__} module, '
                f'{create_vault_access.__name__} method')

    try:
        email_address = data.pop('email_address')

        vault_ = Vault.objects.get(vault_id=vault_id,
                                   email_address=email_address)

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
        logger.error('The entered details are not valid')
        logger.info(f'Exit {__name__} module, '
                    f'{create_vault_access.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} does not exist')
        logger.info(f'Exit {__name__} module, '
                    f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except CustomApiException as e:
        logger.error('The given email address is not belong '
                     'to the organization')
        logger.info(f'Exit {__name__} module, '
                    f'{create_vault_access.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def remove_vault_access(project_id, vault_id, data):
    logger.info(f'Enter {__name__} module, '
                f'{remove_vault_access.__name__} method')

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
        logger.error('The vault access does not exist '
                     'for the given credentials')
        logger.info(f'Exit {__name__} module, '
                    f'{remove_vault_access.__name__} method')
        return Response('No such vault access exist')
    except (ValidationError, KeyError):
        logger.error('The given email address is not belong '
                     'to the organization')
        logger.info(f'Exit {__name__} module, '
                    f'{remove_vault_access.__name__} method')
        return CustomApiException(500, 'Enter valid details')


def get_vault_access(vault_id, email_address):
    logger.info(f'Enter {__name__} module, {get_vault_access.__name__} method')

    try:
        vault_access = VaultAccess.objects.get(vault=vault_id,
                                               employee=email_address,
                                               active=True)
        logger.info(f'Exit {__name__} module, '
                    f'{get_vault_access.__name__} method')
        return vault_access
    except ObjectDoesNotExist:
        logger.error('Vault Access for the given credentials does not exist')
        logger.info(f'Enter {__name__} module, '
                    f'{get_vault_access.__name__} method')
        return None


def create_component_access(vault_id, component_id, data):
    logger.info(f'Enter {__name__} module, '
                f'{create_component_access.__name__} method')

    try:
        email_address = data.pop('email_address')

        vault = Vault.objects.get(vault_id=vault_id,
                                  email_address=email_address)

        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id)

        employee = employee_service.is_organization_employee(email_address)

        if employee is None:
            raise CustomApiException(404, 'This user is not belong '
                                          'to the organization')

        data['employee'] = email_address
        data['component'] = component_id

        component_access_serializer = ComponentAccessSerializer(data=data)
        component_access_serializer.is_valid(raise_exception=True)
        component_access_serializer.save()

        return component_access_serializer.data
    except Vault.DoesNotExist:
        logger.error('The entered credentials can\'t create component access')
        logger.info(f'Exit {__name__} module, '
                    f'{create_component_access.__name__} method')
        raise CustomApiException(400, 'You don\'t have access '
                                      'to create component access')
    except Component.DoesNotExist:
        logger.error(f'Component for Component ID : {component_id}'
                     f'is not exist')
        logger.info(f'Exit {__name__} module, '
                    f'{create_component_access.__name__} method')
        raise CustomApiException(404, 'Component does not exist')
    except (ValidationError, KeyError):
        logger.error('Entered details are not valid')
        logger.info(f'Exit {__name__} module, '
                    f'{create_component_access.__name__} method')
        raise CustomApiException(500, 'Enter valid details')
    except CustomApiException as e:
        logger.error('The given email address is not belong '
                     'to the organization')
        logger.info(f'Exit {__name__} module, '
                    f'{create_component_access.__name__} method')
        raise CustomApiException(e.status_code, e.detail)


def remove_component_access(vault_id, component_id, data):
    logger.info(f'Enter {__name__} module, '
                f'{remove_component_access.__name__} method')

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
        logger.error('No component access was provided for the given details')
        logger.info(f'Exit {__name__} module, '
                    f'{remove_component_access.__name__} method')
        return Response('No such component access exist')
    except (ValidationError, KeyError):
        logger.error('Entered details are not valid')
        logger.info(f'Exit {__name__} module, '
                    f'{remove_component_access.__name__} method')
        raise CustomApiException(500, 'Enter valid details')


def get_component_access(component_id, email_address):
    try:
        component = ComponentAccess.objects.get(component_id=component_id,
                                                employee=email_address,
                                                active=True)
        return component
    except ObjectDoesNotExist:
        return None
