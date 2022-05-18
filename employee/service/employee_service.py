"""this module is used to create, update and delete employee details
"""
import logging

from rest_framework.exceptions import ValidationError

from credential.models import VaultAccess
from credential.serializers import VaultResponseSerializer
from employee.models import Employee
from employee.serializers import EmployeeSerializer, EmployeeResponseSerializer

from organization.models import Organization

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_employee(organization_id, data):
    """used to create employee in an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{create_employee.__name__} method')

        organization = Organization.objects.get(
            organization_id=organization_id, active=True,
        )

        data['created_by'] = organization.organization_id
        data['organization'] = organization.organization_id

        employee_serializer = EmployeeSerializer(data=data)
        employee_serializer.is_valid(raise_exception=True)
        employee_serializer.save()

        logger.debug('Employee creation successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_employee.__name__} method')

        return employee_serializer.data
    except (ValidationError, KeyError):
        logger.error('Enter valid details. Employee creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_employee.__name__} method')
        raise CustomApiException(500, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist. Employee creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_employee.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


def get_employee(organization_id, data):
    """used to get employee details and associated vaults using employee email
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{get_employee.__name__} method')

        email = data.get("email")

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True,
        )

        employee = Employee.objects.get(
            email=email, active=True,
            organization=organization.organization_id,
            organization__active=True
        )

        organization_level_vaults_accesses = VaultAccess.objects.filter(
            access_level='ORGANIZATION',
            active=True,
            organization=organization_id,
            organization__active=True
        )

        project_level_vaults_accesses = VaultAccess.objects.filter(
            access_level='PROJECT',
            active=True,
            organization=organization_id,
            organization__active=True,
            project__employees__employee_id=employee.employee_id
        )

        individual_level_vault_accesses = VaultAccess.objects.filter(
            access_level='INDIVIDUAL',
            active=True,
            organization=organization_id,
            organization__active=True,
            employee=employee.employee_id
        )

        organization_level_vaults = [
            organization_vault_access.vault
            for organization_vault_access in organization_level_vaults_accesses
        ]

        project_level_vaults = [
            project_vault_access.vault
            for project_vault_access in project_level_vaults_accesses
        ]

        individual_level_vaults = [
            individual_level_vault_access.vault
            for individual_level_vault_access
            in individual_level_vault_accesses
        ]

        employee_serializer = EmployeeResponseSerializer(employee)

        response_employee = employee_serializer.data

        response_employee['organization_vaults'] \
            = VaultResponseSerializer(organization_level_vaults, many=True) \
            .data

        response_employee['project_vaults'] \
            = VaultResponseSerializer(project_level_vaults, many=True) \
            .data

        response_employee['individual_vaults'] \
            = VaultResponseSerializer(individual_level_vaults, many=True) \
            .data

        logger.debug(f'Exit {__name__} module, {get_employee.__name__} method')

        return response_employee
    except ValidationError:
        logger.error('Load valid details in the file. '
                     'Employees creation failure')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(500, 'Load valid details in the file')
    except KeyError:
        logger.error('Enter valid details. Employees creation failure')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error('Employee not exist')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
