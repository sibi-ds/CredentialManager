"""This module is used to create, update and delete
components of a vault
"""
import logging

from rest_framework.exceptions import ValidationError

from credential.models import Component
from credential.models import Vault

from credential.serializers import ComponentSerializer

from employee.service import employee_service
from credential.service import user_access_service

from credential.utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_component(vault_id, data):
    """used to create component for a vault
    """
    logger.info(f'Enter {__name__} module, {create_component.__name__} method')

    try:
        vault = Vault.objects.get(vault_id=vault_id, active=True)

        data['vault'] = vault_id

        component_serializer = ComponentSerializer(data=data)
        component_serializer.is_valid(raise_exception=True)
        component_serializer.save()
        logger.info(f'Exit {__name__} module, '
                    f'{create_component.__name__} method')

        return component_serializer.data
    except ValidationError:
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'Vault with Vault ID:  {vault_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_component.__name__} method')
        raise CustomApiException(400, 'No such vault exist')


def get_component(vault_id, component_id, data):
    """used to get component and its items from a vault
    """
    logger.info(f'Enter {__name__} module, {get_component.__name__} method')

    try:
        email = data.get('email')

        vault = Vault.objects.get(vault_id=vault_id, active=True)

        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id,
                                          active=True)

        response_component = None

        if vault.employee.email == email:
            response_component = component
        elif (vault.access_level.access_level == 'ORGANIZATION'
              or component.access_level.access_level == 'ORGANIZATION') \
                and employee_service \
                .is_organization_employee(email) is not None:
            response_component = component
        elif (vault.project is not None
              and vault.access_level.access_level == 'PROJECT'
              or component.access_level.access_level == 'PROJECT') \
                and employee_service \
                .is_project_employee(email, vault.project.project_id) \
                is not None:
            response_component = component
        elif user_access_service.get_vault_access(vault_id, email) \
                is not None:
            response_component = component
        elif user_access_service.get_component_access(component_id, email) \
                is not None:
            response_component = component

        if response_component is None:
            logger.error('You don\'t have access for this component')
            raise CustomApiException(400,
                                     "You don't have access for this "
                                     "component")

        component_serializer = ComponentSerializer(response_component)
        logger.info(f'Exit {__name__} module, '
                    f'{get_component.__name__} method')

        return component_serializer.data
    except KeyError:
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{get_component.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
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


def update_component(vault_id, component_id, data):
    """used to update component details and items
    """
    logger.info(f'Enter {__name__} module, '
                f'{update_component.__name__} method')

    try:
        vault = Vault.objects.get(vault_id=vault_id, active=True)

        component = Component.objects.get(component_id=component_id)

        component_serializer = ComponentSerializer(instance=component,
                                                   data=data)

        component_serializer.is_valid(raise_exception=True)
        component_serializer.save()

        logger.info('Component details updated successfully')
        logger.info(f'Exit {__name__} module, '
                    f'{update_component.__name__} method')

        return component_serializer.data
    except (ValidationError, KeyError):
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error('The entered credentials don\'t have access '
                     'for the component')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Component.DoesNotExist:
        logger.error(f'Component for Component ID : {component_id}'
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_component.__name__} method')
        raise CustomApiException(404, 'No such component exist')


def change_active_status(vault_id, component_id, data):
    """used to change active status of a component
    """
    logger.info(f'Enter {__name__} module, '
                f'{change_active_status.__name__} method')

    try:
        email = data.get('email')
        active = data.get('active')

        vault = Vault.objects.get(vault_id=vault_id, active=True)
        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id)

        if vault.employee.email == email:
            component.active = active
            component.save()
            return active
        else:
            logger.error('You don\'t have access to change active status')
            raise CustomApiException(400, 'You don\'t have access'
                                          'to change active status')
    except KeyError:
        logger.error('Entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault ID : {vault_id} is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Component.DoesNotExist:
        logger.error(f'Component for Component ID : {component_id} '
                     f'is not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(404, 'No such component exist')
    except CustomApiException as e:
        logger.error('Entered credentials don\'t have access '
                     'to change component active status')
        logger.error(f'Exit {__name__} module, '
                     f'{change_active_status.__name__} method')
        raise CustomApiException(e.status_code, e.detail)
