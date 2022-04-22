import logging

from django.core.exceptions import ObjectDoesNotExist

from employee.models import EmployeeAccount

logger = logging.getLogger('credential-manager-logger')


def is_organization_employee(email_address):
    logger.info(f'Enter {__name__} module, '
                f'{is_organization_employee.__name__} method')

    try:
        employee = EmployeeAccount.objects.get(email=email_address)
        logger.info(f'Exit {__name__} module, '
                    f'{is_organization_employee.__name__} method')
        return employee
    except ObjectDoesNotExist:
        logger.error('The given email address is not belong '
                     'to the organization')
        logger.info(f'Exit {__name__} module, '
                    f'{is_organization_employee.__name__} method')
        return None


def is_project_employee(email_address, project_id):
    logger.info(f'Enter {__name__} module, '
                f'{is_project_employee.__name__} method')

    try:
        employee = EmployeeAccount.objects.get(projects__project_id=project_id,
                                               email=email_address)
        logger.info(f'Exit {__name__} module, '
                    f'{is_project_employee.__name__} method')
        return employee
    except ObjectDoesNotExist:
        logger.error('The given email address is not belong to the project')
        logger.info(f'Exit {__name__} module, '
                    f'{is_project_employee.__name__} method')
        return None