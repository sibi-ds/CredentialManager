import logging

from django.http import HttpRequest
from oauth2_provider.models import AccessToken

from rest_framework.decorators import api_view
from rest_framework.response import Response

from client.models import Client
from client.service import client_service
from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST'])
def create_client(request: HttpRequest):
    """used to create organization
    """
    try:
        logger.debug(f'Enter {__name__} module, create_client method')
        client = client_service.create_client(request.data)
        logger.debug(f'Exit {__name__} module, create_client method')
        return Response(client)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_client method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET'])
def get_client(request: HttpRequest):
    application = Client.objects.get(id=5)
    token = AccessToken.objects.create(application=application)
    print(token)
    return Response(token.token)

