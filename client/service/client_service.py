import logging

from rest_framework.exceptions import ValidationError

from client.models import Client
from client.serializers import ClientSerializer
from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


def create_client(data):
    """used to create organization
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{create_client.__name__} method')

        # client_serializer = ClientSerializer(data=data)
        # client_serializer.is_valid(raise_exception=True)
        # client_serializer.save()
        client = Client.objects.create(**data)
        client_serializer = ClientSerializer(client)

        logger.debug('Client creation successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_client.__name__} method')

        return client_serializer.data
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Organization creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_client.__name__} method')
        raise CustomApiException(400, message)