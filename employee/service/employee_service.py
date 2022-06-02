"""this module is used to create, update and delete employee details
"""
import logging

from rest_framework.exceptions import ValidationError

from credential.models import VaultAccess
from credential.serializers import VaultResponseSerializer

from employee.models import Employee
from employee.serializers import EmployeeResponseSerializer
from employee.serializers import EmployeeSerializer

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
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Employee creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_employee.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{create_employee.__name__} method')
        raise CustomApiException(400, message)
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

        email = data["email"]

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True,
        )

        employee = Employee.objects.get(
            email=email, active=True,
            organization=organization,
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
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Employees fetch failure')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(500, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{get_employee.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error('Employee not exist')
        logger.error(f'Exit {__name__} module, {get_employee.__name__} method')
        raise CustomApiException(404, 'No such employee exist')


def get_employees(organization_id, data):
    """used to get all projects from an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{get_employees.__name__} method')

        email = data['email']

        organization = Organization.objects.get(
            organization_id=organization_id, active=True, email=email
        )

        employees = Employee.objects.filter(organization=organization,
                                            active=True)

        employee_serializer = EmployeeSerializer(employees, many=True)

        logger.debug(f'Exit {__name__} module, '
                     f'{get_employees.__name__} method')

        return employee_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{get_employees.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{get_employees.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_employees.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


def update_employee_status(organization_id, employee_uid, data):
    """used to update employee status
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{update_employee_status.__name__} method')

        email = data.get("email")

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        employee = Employee.objects.get(
            employee_uid=employee_uid,
            organization=organization
        )

        employee.active = not employee.active
        employee.save()

        employee_serializer = EmployeeSerializer(employee)

        logger.debug('Employee status updated successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_employee_status.__name__} method')

        return employee_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details.Employee status update failure')
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee_status.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee_status.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee_status.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error('No such employee exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee_status.__name__} method')
        raise CustomApiException(400, 'No such employee exist')


def update_employee(organization_id, employee_uid, data):
    """used to update employee status
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{update_employee.__name__} method')

        email = data["email"]

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        employee = Employee.objects.get(
            employee_uid=employee_uid,
            organization=organization,
            active=True
        )

        employee_serializer = EmployeeSerializer(employee, data=data,
                                                 partial=True)
        employee_serializer.is_valid(raise_exception=True)
        employee_serializer.save()

        logger.debug('Employee details updated successfully')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_employee.__name__} method')

        return employee_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Employee update failure')
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error('No such employee exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_employee.__name__} method')
        raise CustomApiException(400, 'No such employee exist')
