"""this module is used to create, update and delete project details
"""
import logging

from rest_framework.exceptions import ValidationError

from employee.models import Employee

from project.models import Project
from project.serializers import ProjectOnlySerializer
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
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Project creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(500, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('Organization not exist. Project creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


def get_project(organization_id, project_uid, data):
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
            project_uid=project_uid, active=True,
        )

        project_serializer = ProjectSerializer(project)

        logger.debug(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')

        return project_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')
        raise CustomApiException(500, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{get_project.__name__} method')
        raise CustomApiException(400, message)
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


def get_projects(organization_id, data):
    """used to get all projects from an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{get_projects.__name__} method')

        email = data['email']

        organization = Organization.objects.get(
            organization_id=organization_id, active=True,
            email=email
        )

        projects = Project.objects.filter(organization=organization,
                                          active=True)

        project_serializer = ProjectOnlySerializer(projects, many=True)

        logger.debug(f'Exit {__name__} module, '
                     f'{get_projects.__name__} method')

        return project_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{get_projects.__name__} method')
        raise CustomApiException(500, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{get_projects.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_projects.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


def assign_employee(organization_id, project_uid, data):
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
            project_uid=project_uid, active=True,
        )

        email = data['email']

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
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')
        raise CustomApiException(500, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{assign_employee.__name__} method')
        raise CustomApiException(400, message)
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


def update_project_status(organization_id, project_uid, data):
    """used to update project status
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{update_project_status.__name__} method')

        email = data["email"]

        organization = Organization.objects.get(
            organization_id=organization_id,
            email=email, active=True
        )

        project = Project.objects.get(
            project_uid=project_uid,
            organization=organization
        )

        project.active = not project.active
        project.save()

        project_serializer = ProjectOnlySerializer(project)

        logger.debug('Project status updated successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_project_status.__name__} method')

        return project_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Project status update failure')
        logger.error(f'Exit {__name__} module, '
                     f'{update_project_status.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{update_project_status.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_project_status.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Project.DoesNotExist:
        logger.error('No such project exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_project_status.__name__} method')
        raise CustomApiException(400, 'No such project exist')


def update_project(organization_id, project_uid, data):
    """used to update project details
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{update_project.__name__} method')

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        project = Project.objects.get(
            project_uid=project_uid,
            organization=organization,
            active=True
        )

        project_serializer = ProjectOnlySerializer(project, data=data,
                                                   partial=True)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()

        logger.debug('Project details updated successfully')
        logger.debug(f'Exit {__name__} module, '
                     f'{update_project.__name__} method')

        return project_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Enter valid details. Project update failure')
        logger.error(f'Exit {__name__} module, '
                     f'{update_project.__name__} method')
        raise CustomApiException(400, message)
    except KeyError as ke:
        message = ke.args[0] + ' is missing'
        logger.error(message)
        logger.error(f'Exit {__name__} module, '
                     f'{update_project.__name__} method')
        raise CustomApiException(400, message)
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_project.__name__} method')
        raise CustomApiException(400, 'No such organization exist')
    except Project.DoesNotExist:
        logger.error('No such project exist')
        logger.error(f'Exit {__name__} module, '
                     f'{update_project.__name__} method')
        raise CustomApiException(400, 'No such project exist')
