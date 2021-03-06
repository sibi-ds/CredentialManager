"""This module is used to achieve vault and component
accesses for the employees in an organization
"""
import logging

from django.db import IntegrityError

from rest_framework.exceptions import ValidationError

from credential.models import Vault
from credential.models import VaultAccess
from credential.serializers import VaultAccessSerializer

from employee.models import Employee

from organization.models import Organization

from project.models import Project

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def get_vault_accesses(organization_id, vault_id):
    """used to get vault access
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_vault_accesses.__name__} method')

    vault_accesses = VaultAccess.objects.filter(
        organization=organization_id, organization__active=True,
        vault=vault_id, vault__active=True,
        active=True
    )

    logger.debug(f'Exit {__name__} module, '
                 f'{get_vault_accesses.__name__} method')

    return vault_accesses


def get_organization_vault_access(organization_id, vault_id):
    """used to get organization vault access
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_organization_vault_access.__name__} method')

    try:
        organization_vault_access = VaultAccess.objects.get(
            organization=organization_id, organization__active=True,
            vault=vault_id, vault__active=True,
            access_level='ORGANIZATION',
            active=True
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{get_organization_vault_access.__name__} method')

        return organization_vault_access
    except VaultAccess.DoesNotExist:
        logger.error('No organization access is provided for this vault')
        logger.error(f'Exit {__name__} module, '
                     f'{get_organization_vault_access.__name__} method')
        return None


def get_project_vault_access(organization_id, vault_id, projects):
    """used to get project vault access
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_project_vault_access.__name__} method')

    try:
        project_ids = [project.project_id for project in projects
                       if project.active]

        project_vault_access = VaultAccess.objects.get(
            organization=organization_id, organization__active=True,
            vault=vault_id, vault__active=True,
            access_level='PROJECT',
            project__project_id__in=project_ids,
            active=True
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{get_project_vault_access.__name__} method')

        return project_vault_access
    except VaultAccess.DoesNotExist:
        logger.error('No project access is given for this vault')
        logger.error(f'Exit {__name__} module, '
                     f'{get_project_vault_access.__name__} method')
        return None


def get_individual_vault_access(organization_id, employee_id, vault_id):
    """used to get individual vault access
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{get_individual_vault_access.__name__} method')

    try:
        individual_employee_vault_access = VaultAccess.objects.get(
            organization=organization_id, organization__active=True,
            vault=vault_id, vault__active=True,
            employee=employee_id, employee__active=True,
            access_level='INDIVIDUAL',
            active=True
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{get_individual_vault_access.__name__} method')

        return individual_employee_vault_access
    except VaultAccess.DoesNotExist:
        logger.error('No individual user access is given for this user')
        logger.error(f'Exit {__name__} module, '
                     f'{get_individual_vault_access.__name__} method')
        return None


def has_vault_access(organization_id, employee, vault_id):
    """used to check employee has the vault access
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{has_vault_access.__name__} method')

    organization_vault_access = get_organization_vault_access(
        organization_id, vault_id)

    project_vault_access = get_project_vault_access(
        organization_id, vault_id, employee.projects.all())

    individual_vault_access = get_individual_vault_access(
        organization_id, employee.employee_id, vault_id)

    if organization_vault_access is not None \
            or project_vault_access is not None \
            or individual_vault_access is not None:

        logger.debug('The given user has access to this vault')
        logger.debug(f'Exit {__name__} module, '
                     f'{has_vault_access.__name__} method')
        return True
    else:
        logger.debug('The given user has no access to this vault')
        logger.debug(f'Exit {__name__} module, '
                     f'{has_vault_access.__name__} method')
        return False


def can_update_vault(organization_id, employee, vault_id):
    """used to check employee has the vault update access
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{has_vault_access.__name__} method')

    organization_vault_access = get_organization_vault_access(
        organization_id, vault_id)

    project_vault_access = get_project_vault_access(
        organization_id, vault_id, employee.projects.all())

    individual_vault_access = get_individual_vault_access(
        organization_id, employee.employee_id, vault_id)

    if (organization_vault_access is not None
            and organization_vault_access.scope == 'READ/WRITE') \
        or (project_vault_access is not None
            and project_vault_access.scope == 'READ/WRITE') \
        or (individual_vault_access is not None
            and individual_vault_access.scope == 'READ/WRITE'):

        logger.debug('The given user has access to edit this vault')
        logger.debug(f'Exit {__name__} module, '
                     f'{has_vault_access.__name__} method')
        return True
    else:
        logger.debug('The given user has no access to edit this vault')
        logger.debug(f'Exit {__name__} module, '
                     f'{has_vault_access.__name__} method')
        return False


def create_vault_access(organization_id, employee_uid, vault_uid, data):
    """used to create vault access for employees
    """
    logger.info(f'Enter {__name__} module, '
                f'{create_vault_access.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        creating_employee = Employee.objects.get(
            employee_uid=employee_uid, active=True,
            organization=organization, organization__active=True,
        )

        vault = Vault.objects.get(
            vault_uid=vault_uid, active=True,
            organization=organization, organization__active=True,
        )

        if creating_employee.employee_id != vault.created_by.employee_id:
            logger.error('Only vault owner can give access')
            logger.error(f'Exit {__name__} module, '
                         f'{create_vault_access.__name__} method')
            raise CustomApiException(400, 'Only vault owner can give access')

        access_level = data['access_level']
        scope = data['scope']

        vault_access = None

        vault_accesses = get_vault_accesses(organization_id, vault.vault_id)

        if access_level == 'ORGANIZATION':

            organization_vault_access = get_organization_vault_access(
                organization_id, vault.vault_id)

            if organization_vault_access is not None \
                    and organization_vault_access.scope == scope:
                raise CustomApiException(400, 'Organization access is '
                                              'already given for this vault')
            else:
                for vault_access in vault_accesses:
                    revoke_vault_access(vault_access)

                vault_access = create_organization_vault_access(
                    organization_id, creating_employee, vault.vault_id, scope)
        elif access_level == 'PROJECT':

            project = Project.objects.get(
                project_id=data['project'], active=True,
                organization=organization, organization__active=True,
            )

            project_vault_access = get_project_vault_access(
                organization_id, vault.vault_id, [project])

            if project_vault_access is not None \
                    and project_vault_access.scope == scope:
                raise CustomApiException(400, 'Project access is already '
                                              'given to this project '
                                              'for this vault')
            else:
                for vault_access in vault_accesses:
                    revoke_vault_access(vault_access)

                vault_access = create_project_vault_access(
                    organization_id, creating_employee, project.project_id,
                    vault.vault_id, scope
                )
        elif access_level == 'INDIVIDUAL':
            email = data['employee']

            employee = Employee.objects.get(
                email=email, active=True,
                organization=organization, organization__active=True,
            )

            individual_vault_access = get_individual_vault_access(
                organization_id, employee.employee_id, vault.vault_id)

            if individual_vault_access is not None \
                    and individual_vault_access.scope == scope:
                raise CustomApiException(400, 'Individual access is already '
                                              'given to the given user '
                                              'for this vault')
            else:
                for vault_access in vault_accesses:
                    if vault_access.access_level == 'PROJECT' \
                            or vault_access.access_level == 'ORGANIZATION'\
                            or (vault_access.access_level == 'INDIVIDUAL'
                                and vault_access.employee.email == email
                                and vault_access.scope != scope):
                        revoke_vault_access(vault_access)

                vault_access = create_individual_vault_access(
                    organization_id, creating_employee, email,
                    vault.vault_id, scope)

        if vault_access is None:
            logger.error('Vault access creation failure')
            logger.error(f'Exit {__name__} module, '
                         f'{create_vault_access.__name__} method')
            raise CustomApiException(500, 'Vault access creation failure')

        vault_access_serializer = VaultAccessSerializer(vault_access)

        logger.info(f'Exit {__name__} module, '
                    f'{create_vault_access.__name__} method')

        return vault_access_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('The entered details are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(400, message)
    except Vault.DoesNotExist:
        logger.error(f'Vault for Vault UID : {vault_uid} does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Employee.DoesNotExist:
        logger.error(f'Employee for Employee UID : {employee_uid} '
                     f'does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
    except Project.DoesNotExist:
        logger.error(f'Project does not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(404, 'No such project exist')
    except Organization.DoesNotExist:
        logger.error(f'Organization with Organization ID: '
                     f'{organization_id} not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{create_vault_access.__name__} method')
        raise CustomApiException(400, 'No such organization exist')


def create_individual_vault_access(organization_id, creating_employee, email,
                                   vault_id, scope):
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
            scope=scope
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
                                vault_id, scope):
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
            project=project,
            scope=scope
        )

        logger.debug('Vault access creation successful')
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
                                     vault_id, scope):
    """used to create vault access for organization employees
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_organization_vault_access.__name__} method')

    try:
        vault_access = VaultAccess.objects.create(
            organization_id=organization_id,
            vault_id=vault_id,
            access_level='ORGANIZATION',
            created_by=creating_employee,
            scope=scope
        )

        logger.debug(f'Exit {__name__} module, '
                     f'{create_organization_vault_access.__name__} method')

        return vault_access
    except IntegrityError:
        logger.error('Vault access creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_organization_vault_access.__name__} method')
        return None


def remove_vault_access(organization_id, employee_uid, vault_uid):
    """used to remove vault access of a vault
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{remove_vault_access.__name__} method')

    try:
        organization = Organization.objects.get(
            organization_id=organization_id, active=True
        )

        vault_owner = Employee.objects.get(
            employee_uid=employee_uid,
            active=True,
            organization=organization_id,
        )

        vault = Vault.objects.get(
            vault_uid=vault_uid, active=True,
            organization=organization
        )

        vault_accesses = VaultAccess.objects.filter(
            organization=organization_id,
            vault=vault.vault_id,
            created_by=vault_owner,
            active=True
        )

        for vault_access in vault_accesses:
            if vault_owner.employee_id != vault_access.created_by.employee_id:
                logger.error('Only vault owner can remove access')
                raise CustomApiException(400,
                                         'Only vault owner can remove access')

            revoke_vault_access(vault_access)

        vault_access_serializer = VaultAccessSerializer(vault_accesses,
                                                        many=True)

        logger.debug('Vault accesses removed successfully')
        logger.debug(f'Exit {__name__} module, '
                     f'{remove_vault_access.__name__} method')

        return vault_access_serializer.data
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_vault_access.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Vault.DoesNotExist:
        logger.error('No such vault exist')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_vault_access.__name__} method')
        raise CustomApiException(404, 'No such vault exist')
    except Employee.DoesNotExist:
        logger.error('No such employee exist')
        logger.error(f'Exit {__name__} module, '
                     f'{remove_vault_access.__name__} method')
        raise CustomApiException(404, 'No such employee exist')


def revoke_vault_access(vault_access):
    """used to remove vault access given to a vault
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{revoke_vault_access.__name__} method')

        vault_access.active = False
        vault_access.updated_by = vault_access.created_by
        vault_access.save()

        logger.debug(f'Exit {__name__} module, '
                     f'{revoke_vault_access.__name__} method')
    except IntegrityError:
        logger.error('Vault access removal failure')
        logger.error(f'Exit {__name__} module, '
                     f'{revoke_vault_access.__name__} method')
        raise CustomApiException(500, 'Vault access removal failure')
