import logging

from credential.models import Employee


logger = logging.getLogger('credential-manager-logger')


def get_organization_employee(organization_id, email):
    logger.info(f'Enter {__name__} module, '
                f'{get_organization_employee.__name__} method')

    try:
        employee = Employee.objects.get(
            email=email, active=True,
            organization__organization_id=organization_id,
            organization__active=True
        )

        logger.info(f'Exit {__name__} module, '
                    f'{get_organization_employee.__name__} method')
        return employee
    except Employee.DoesNotExist:
        logger.error('The given email address is not belong '
                     'to the organization')
        logger.error(f'Exit {__name__} module, '
                     f'{get_organization_employee.__name__} method')
        return None


def is_project_employee(organization_id, project_id, email):
    logger.info(f'Enter {__name__} module, '
                f'{is_project_employee.__name__} method')

    try:
        employee = Employee.objects.get(
            projects__project_id=project_id,
            email=email, active=True,
            organization__organization_id=organization_id,
            organization__active=True
        )

        logger.info(f'Exit {__name__} module, '
                    f'{is_project_employee.__name__} method')
        return employee
    except Employee.DoesNotExist:
        logger.error('The given email address is not belong to the project')
        logger.error(f'Exit {__name__} module, '
                     f'{is_project_employee.__name__} method')
        return None


def get_employee(organization_id, email):
    try:
        logger.info(f'Enter {__name__} module, '
                    f'{get_employee.__name__} method')

        employee = Employee.objects.get(
            email=email, active=True,
            organization__organization_id=organization_id
        )

        logger.info(f'Exit {__name__} module, '
                    f'{get_employee.__name__} method')

        return employee
    except Employee.DoesNotexist:
        logger.error('Entered credentials are not valid')
        logger.error(f'Exit {__name__} module, '
                     f'{get_employee.__name__} method')

        return None
