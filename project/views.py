"""this module is used to do project related operations
"""
import logging

from django.db import IntegrityError
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from files import file_reader

from organization.models import Organization

from project.models import Project
from project.serializers import ProjectSerializer

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


@api_view(['POST'])
def create_project(request: HttpRequest):
    """used to create project in an organization
    """
    try:
        logger.info(f'Enter {__name__} module, '
                    'create_project method')
        name = request.data.get("name")
        email = request.data.get("email")
        description = request.data.get("description")

        project = Project.objects.create(name=name, email=email,
                                         description=description)
        project_serializer = ProjectSerializer(project)
        logger.info('Project created successfully')
        logger.info(f'Exit {__name__} module, '
                    f'{create_project.__name__} method')
        return Response(project_serializer.data)
    except KeyError:
        logger.error('Project creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except IntegrityError:
        logger.error('Project creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_project.__name__} method')
        raise CustomApiException(400, 'Project email already exist')
