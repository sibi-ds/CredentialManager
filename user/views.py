import logging

from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.service import user_service
from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


@api_view(['POST', ])
def create_user(request: HttpRequest):
    """used to create employee in an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, create_user method')
        user = user_service.create_user(request.data)
        logger.debug(f'Exit {__name__} module, create_user method')
        return Response(user)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_user method')
        raise CustomApiException(e.status_code, e.detail)
