"""this module is used to create, update and delete project details
"""
import logging

from rest_framework.exceptions import ValidationError

from employee.models import Employee
from project.models import Project
from project.serializers import ProjectSerializer

from organization.models import Organization

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


def create_project(organization_id, data):
    """used to create project in an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{create_project.__name__} method')

        organization = Organization.objects.get(
            organization_id=organization_id, active=True,
        )

        data['created_by'] = organization.organization_id
        data['organization'] = organization.organization_id

        project_serializer = ProjectSerializer(data=data)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()

        logger.debug('Project creation successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')

        return project_serializer.data
    except (ValidationError, KeyError):
        logger.error('Enter valid details. Project creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(500, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist. Project creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


def get_project(organization_id, project_id, data):
    """used to get project from an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{get_project.__name__} method')

        organization = Organization.objects.get(
            organization_id=organization_id, active=True,
        )

        project = Project.objects.get(
            organization=organization, organization__active=True,
            project_id=project_id, active=True,
        )

        email = data.get('employee')

        employee = Employee.objects.get(
            organization=organization, organization__active=True,
            email=email, active=True,
        )

        project_serializer = ProjectSerializer(project)

        logger.debug(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')

        return project_serializer.data
    except (ValidationError, KeyError):
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')
        raise CustomApiException(500, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Project.DoesNotExist:
        logger.error('Project not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')
        raise CustomApiException(404, 'No such project exist')
    except Employee.DoesNotExist:
        logger.error('Employee not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')
        raise CustomApiException(404, 'No such employee exist')


def assign_employee(organization_id, project_id, data):
    """used to assign employee to a project
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{assign_employee.__name__} method')

        organization = Organization.objects.get(
            organization_id=organization_id, active=True,
        )

        project = Project.objects.get(
            organization=organization, organization__active=True,
            project_id=project_id, active=True,
        )

        email = data.get('employee')

        employee = Employee.objects.get(
            organization=organization, organization__active=True,
            email=email, active=True,
        )

        for assigned_employee in project.employees.all():
            if assigned_employee.employee_id == employee.employee_id:
                raise CustomApiException(400, 'Employee already assigned '
                                              'to this project')

        project.employees.add(employee)
        project.save()

        project_serializer = ProjectSerializer(project)

        logger.debug('Employee assigned successfully')
        logger.debug(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')

        return project_serializer.data
    except (ValidationError, KeyError):
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')
        raise CustomApiException(500, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')
        raise CustomApiException(404, 'No such organization exist')
    except Project.DoesNotExist:
        logger.error('Project not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')
        raise CustomApiException(404, 'No such project exist')
    except Employee.DoesNotExist:
        logger.error('Employee not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')
        raise CustomApiException(404, 'No such employee exist')
