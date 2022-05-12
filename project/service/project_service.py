"""this module is used to create, update and delete project details
"""
import logging

from rest_framework.exceptions import ValidationError

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
