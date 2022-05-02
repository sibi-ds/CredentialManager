"""This module is used to achieve vault and component
accesses for the employees in an organization
"""
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from credential.models import Vault
from credential.models import VaultAccess

from credential.serializers import VaultAccessSerializer
from employee.models import Employee
from organization.models import Organization
from project.models import Project

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def get_admin_vault_access(organization_id, employee_id, vault_id):
    """used to get vault access of vault owner
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_admin_vault_access.__name__} method')

    try:
        vault_access = VaultAccess.objects.get(
            organization=organization_id, organization__active=True,
            vault=vault_id, vault__active=True,
            created_by=employee_id,
            access_level=None
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{get_admin_vault_access.__name__} method')

        return vault_access
    except VaultAccess.DoesNotExist:
        logger.error('No admin vault access exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_admin_vault_access.__name__} method')
        return None


def get_organization_vault_accesses(organization_id, vault_id):
    """used to get organization vault accesses
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_organization_vault_accesses.__name__} method')

    vault_accesses = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        access_level='ORGANIZATION',
    )

    logger.debug(f'Exit {__name__} module, '
                 f'{get_organization_vault_accesses.__name__} method')

    return vault_accesses


def get_project_vault_accesses(organization_id, vault_id, projects):
    """used to get project vault accesses
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_project_vault_accesses.__name__} method')

    project_ids = [project.project_id for project in projects]

    vault_accesses = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        access_level='PROJECT',
        project__project_id__in=project_ids,
    )

    logger.debug(f'Exit {__name__} module, '
                 f'{get_project_vault_accesses.__name__} method')

    return vault_accesses


def get_individual_vault_accesses(organization_id, employee_id, vault_id):
    """used to get individual vault accesses
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_individual_vault_accesses.__name__} method')

    vault_accesses = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        employee__employee_id=employee_id,
        access_level='INDIVIDUAL',
    )

    logger.debug(f'Exit {__name__} module, '
                 f'{get_individual_vault_accesses.__name__} method')

    return vault_accesses


def create_vault_access(organization_id, uid, vault_id, data):
    """used to create vault access for employees
    """
    logger.info(f'Enter {__name__} module, '
                f'{create_vault_access.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        creating_employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization, organization__active=True,
        )

        vault = Vault.objects.get(
            vault_id=vault_id, active=True,
            organization=organization, organization__active=True,
        )

        if creating_employee.employee_id != vault.created_by.employee_id:
            logger.error('Only vault owner can give access')
            logger.error(f'Exit {__name__} module, '
                         f'{create_vault_access.__name__} method')
            raise CustomApiException(400, 'Only vault owner can give access')

        access_level = data.pop('access_level')

        vault_access = None

        if access_level == 'ORGANIZATION':
            vault_access = create_organization_vault_access(organization_id,
                                                            creating_employee,
                                                            vault_id)
        elif access_level == 'PROJECT':
            vault_access = create_project_vault_access(organization_id,
                                                       creating_employee,
                                                       data.pop('project'),
                                                       vault_id)
        elif access_level == 'INDIVIDUAL':
            email = data.pop('employee')

            vault_access = create_individual_vault_access(organization_id,
                                                          creating_employee,
                                                          email, vault_id)

        if vault_access is None:
            logger.error('Vault access creation failure')
            logger.error(f'Exit {__name__} module, '
                         f'{create_vault_access.__name__} method')
            raise CustomApiException(500, 'Vault access creation failure')

        vault_access_serializer = VaultAccessSerializer(vault_access)

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
    except Employee.DoesNotExist:
        logger.error(f'Employee for Employee UID : {uid} does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except Organization.DoesNotExist:
        logger.error(f'Organization with Organization ID: '
                     f'{organization_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(400, 'No such organization exist')


def create_individual_vault_access(organization_id, creating_employee, email,
                                   vault_id):
    """used to create vault access for individual employee
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_individual_vault_access.__name__} method')

    try:
        employee = Employee.objects.get(
            email=email, active=True,
            organization=organization_id,
            organization__active=True
        )

        vault_access = VaultAccess.objects.create(
            employee=employee,
            organization_id=organization_id,
            vault_id=vault_id,
            access_level='INDIVIDUAL',
            created_by=creating_employee,
        )

        logger.debug(f'Enter {__name__} module, '
                     f'{create_individual_vault_access.__name__} method')

        return vault_access
    except Employee.DoesNotExist:
        logger.error('No such employee exist with the given email address')
        logger.error(f'Exit {__name__} module, '
                     f'{create_individual_vault_access.__name__} method')
        return None
    except IntegrityError:
        logger.error('Vault access creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_individual_vault_access.__name__} method')
        return None


def create_project_vault_access(organization_id, creating_employee, project_id,
                                vault_id):
    """used to create vault access for project employee
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_project_vault_access.__name__} method')

    try:
        project = Project.objects.get(
            project_id=project_id, active=True,
            organization__organization_id=organization_id,
            organization__active=True
        )

        vault_access = VaultAccess.objects.create(
            organization_id=organization_id,
            vault_id=vault_id,
            access_level='PROJECT',
            created_by=creating_employee,
            project=project
        )

        logger.error('Vault access creation successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_project_vault_access.__name__} method')

        return vault_access
    except Project.DoesNotExist:
        logger.error(f'Project for Project ID : {project_id} does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project_vault_access.__name__} method')
        raise CustomApiException(404, 'No such project exist')
    except IntegrityError:
        logger.error('Vault access creation failure')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_project_vault_access.__name__} method')
        return None


def create_organization_vault_access(organization_id, creating_employee,
                                     vault_id):
    """used to create vault access for organization employees
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_organization_vault_access.__name__} method')

    try:
        vault_access = VaultAccess.objects.create(
            organization_id=organization_id,
            vault_id=vault_id,
            access_level='ORGANIZATION',
            created_by=creating_employee
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{create_organization_vault_access.__name__} method')

        return vault_access
    except IntegrityError:
        logger.error('Vault access creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_organization_vault_access.__name__} method')
        return None


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


def update_vault_access(organization_id, uid, vault_id, vault_access_id, data):
    logger.debug(f'Enter {__name__} module, '
                 f'{update_vault_access.__name__} method')

    try:
        vault_access = VaultAccess.objects.get(
            vault_access_id=vault_access_id,
            organization=organization_id,
            vault=vault_id,
            created_by__employee_uid=uid
        )

        vault_access_serializer = VaultAccessSerializer(instance=vault_access,
                                                        data=data,
                                                        partial=True)
        vault_access_serializer.is_valid(raise_exception=False)
        print(vault_access_serializer.errors)
        vault_access_serializer.save()

        logger.debug('Vault access updated successfully')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_vault_access.__name__} method')

        return vault_access_serializer.data
    except VaultAccess.DoesNotExist:
        logger.error('No vault access found')
        logger.error(f'Exit {__name__} module, '
                     f'{update_vault_access.__name__} method')
        raise CustomApiException(404, 'No vault access found')


def delete_vault_access(organization_id, uid, vault_id, vault_access_id):
    logger.debug(f'Enter {__name__} module, '
                 f'{delete_vault_access.__name__} method')

    try:
        vault_owner = Employee.objects.get(
            employee_uid=uid,
            active=True,
            organization=organization_id,
        )

        vault_access = VaultAccess.objects.get(
            vault_access_id=vault_access_id,
            organization=organization_id,
            vault=vault_id,
            created_by=vault_owner
        )

        if not vault_owner.employee_id == vault_access.created_by.employee_id:
            logger.error('Only vault owner can remove access')
            raise CustomApiException(400, 'Only vault owner can remove access')

        vault_access.delete()

        logger.debug('Vault access removed successfully')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_vault_access.__name__} method')

        return 'Vault access deletion successful'
    except VaultAccess.DoesNotExist:
        logger.error('No vault access found')
        logger.error(f'Exit {__name__} module, '
                     f'{delete_vault_access.__name__} method')
        raise CustomApiException(404, 'No vault access found')
    except Employee.DoesNotExist:
        logger.error('No such employee exist')
        logger.error(f'Exit {__name__} module, '
                     f'{delete_vault_access.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
