"""this module is used to do project related operations
"""
import logging

from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from files import file_reader

from organization.models import Organization

from project.models import Project
from project.serializers import ProjectSerializer
from project.serializers import ProjectOnlySerializer
from project.service import project_service

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST', ])
def create_projects(request: HttpRequest):
    """used to create projects using projects csv file
    """
    try:
        logger.debug(f'Enter {__name__} module, create_employees method')

        email = request.data.get("email")

        project_datas = file_reader.create_projects()

        organization_id = request.query_params.get('organization_id')

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True,
            email=email
        )

        for project in project_datas:
            project['organization'] = organization.organization_id
            project['created_by'] = organization.organization_id

        project_list_serializer = ProjectSerializer(
            data=project_datas, many=True
        )

        project_list_serializer.is_valid(raise_exception=True)
        project_list_serializer.save()

        logger.debug('Projects creation successful')

        return Response(project_list_serializer.data)
    except ValidationError:
        logger.error('Load valid details in the file. '
                     'Projects creation failure')
        logger.error(f'Exit {__name__} module, create_projects method')
        raise CustomApiException(500, 'Load valid details in the file')
    except KeyError:
        logger.error('Enter valid details.Projects creation failure')
        logger.error(f'Exit {__name__} module, create_projects method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist.Projects creation failure')
        logger.error(f'Exit {__name__} module, create_projects method')
        raise CustomApiException(404, 'No such organization exist')


@api_view(['GET'])
def get_projects(request: HttpRequest):
    """used to get all vaults from an organization
    """
    logger.debug(f'Enter {__name__} module, get_projects method')

    try:
        organization_id = request.query_params.get('organization_id')
        project_serializer = project_service.get_projects(
            organization_id, request.data
        )
        logger.debug(f'Exit {__name__} module, get_projects method')
        return Response(project_serializer)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, get_projects method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['POST'])
def create_project(request: HttpRequest):
    """used to create project in an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, create_project method')
        organization_id = request.query_params.get('organization_id')
        project = project_service.create_project(organization_id,
                                                 request.data)
        logger.debug(f'Exit {__name__} module, create_project method')
        return Response(project)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_project method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['PATCH'])
def assign_employee(request: HttpRequest, project_uid):
    """used to assign employee to a project
    """
    try:
        logger.debug(f'Enter {__name__} module, assign_employee method')
        organization_id = request.query_params.get('organization_id')
        project = project_service.assign_employee(organization_id,
                                                  project_uid,
                                                  request.data)
        logger.debug(f'Exit {__name__} module, assign_employee method')
        return Response(project)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, assign_employee method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET', 'PUT', 'PATCH'])
def do_project(request: HttpRequest, project_uid):
    logger.debug(f'Enter {__name__} module, do_project method')
    organization_id = request.query_params.get('organization_id')

    if request.method == 'GET':
        try:
            project = project_service.get_project(organization_id,
                                                  project_uid, request.data)
            logger.debug(f'Exit {__name__} module, do_project method')
            return Response(project)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_project method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PUT':
        """used to update project details
        """
        try:
            project_serializer = project_service.update_project(
                organization_id, project_uid, request.data
            )
            logger.debug(f'Exit {__name__} module, do_employee method')
            return Response(project_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_employee method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        """used to update project status
        """
        try:
            project_serializer = project_service.update_project_status(
                organization_id, project_uid, request.data
            )
            logger.debug(f'Exit {__name__} module, do_project method')
            return Response(project_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_project method')
            raise CustomApiException(e.status_code, e.detail)
