"""this module is used to create, update and delete employee details
"""
import logging

from rest_framework.exceptions import ValidationError

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
