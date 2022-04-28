"""This module is used to achieve vault and component
accesses for the employees in an organization
"""
import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from credential.models import Vault
from credential.models import VaultAccess

from credential.serializers import VaultAccessSerializer
from employee.models import Employee
from project.models import Project

from utils.api_exceptions import CustomApiException

from employee.service import employee_service

logger = logging.getLogger('credential-manager-logger')


def get_vault_accesses(organization_id, employee_id, vault_id, access_level):
    vault_accesses = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        created_by___employee__employee_id=employee_id,
        access_level=access_level,
    )

    return vault_accesses


def get_admin_vault_access(organization_id, employee_id, vault_id):
    try:
        vault_access = VaultAccess.objects.get(
            organization=organization_id, organization__active=True,
            vault=vault_id, vault__active=True,
            created_by=employee_id,
            access_level=None
        )

        return vault_access
    except VaultAccess.DoesNotExist:
        return None


def get_organization_vault_accesses(organization_id, vault_id):
    vault_accesses = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        access_level='ORGANIZATION',
    )

    return vault_accesses


def get_project_vault_accesses(organization_id, vault_id,
                               projects):
    project_ids = [project.project_id for project in projects]

    vault_access = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        access_level='PROJECT',
        project__project_id__in=project_ids,
    )
    print(vault_access)

    return vault_access


def get_individual_vault_accesses(organization_id, employee_id, vault_id):
    vault_access = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        employee__employee_id=employee_id,
        access_level='INDIVIDUAL',
    )

    return vault_access


def create_vault_access(organization_id, uid, vault_id, data):
    """used to create vault access for an employee
    """
    logger.info(f'Enter {__name__} module, '
                f'{create_vault_access.__name__} method')

    try:
        creating_employee = Employee.objects.get(
            employee_uid=uid, active=True,
            organization=organization_id, organization__active=True,
        )

        vault = Vault.objects.get(
            vault_id=vault_id, active=True,
            organization=organization_id, organization__active=True,
        )

        if creating_employee.employee_id != vault.created_by.employee_id:
            raise CustomApiException(400, 'Only vault owner can give access')

        access_level = data.pop('access_level')

        vault_access = None

        if access_level == 'ORGANIZATION':
            vault_access = create_organization_vault_access(organization_id,
                                                            creating_employee,
                                                            vault_id)
        elif access_level == 'PROJECT':
            project_id = data.pop('project')

            project = Project.objects.get(
                project_id=project_id,active=True,
                organization__organization_id=organization_id,
                organization__active=True
            )

            vault_access = create_project_vault_access(organization_id,
                                                       creating_employee,
                                                       project, vault_id)
        elif access_level == 'INDIVIDUAL':
            email = data.pop('employee')

            vault_access = create_individual_vault_access(organization_id,
                                                          creating_employee,
                                                          email, vault_id)

        vault_access_serializer = VaultAccessSerializer(data=vault_access)
        vault_access_serializer.is_valid()

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
    except Project.DoesNotExist:
        logger.error(f'Project for Project ID : {project_id} does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such project exist')


def create_individual_vault_access(organization_id, creating_employee, email,
                                   vault_id):
    employee = Employee.objects.get(
        email=email, active=True,
        organization__organization_id=organization_id,
        organization__active=True
    )

    vault_access = VaultAccess.objects.create(
        employee=employee,
        organization_id=organization_id,
        vault_id=vault_id,
        access_level='INDIVIDUAL',
        created_by=creating_employee,
    )

    return vault_access


def create_project_vault_access(organization_id, creating_employee, project,
                                vault_id):
    vault_access = VaultAccess.objects.create(
        organization_id=organization_id,
        vault_id=vault_id,
        access_level='PROJECT',
        created_by=creating_employee,
        project=project
    )

    return vault_access


def create_organization_vault_access(organization_id, creating_employee,
                                     vault_id):
    vault_access = VaultAccess.objects.create(
        organization_id=organization_id,
        vault_id=vault_id,
        access_level='ORGANIZATION',
        created_by=creating_employee
    )

    return vault_access


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
