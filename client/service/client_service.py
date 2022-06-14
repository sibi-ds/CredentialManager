import logging

from django.db import transaction
from oauth2_provider.models import Application
from rest_framework.exceptions import ValidationError

from client.models import Client
from client.serializers import ClientSerializer, ApplicationSerializer
from user.models import User
from user.serializers import UserSerializer
from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


@transaction.atomic
def create_client(super_user_id, data):
    """used to create client and it's admin user
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{create_client.__name__} method')

        admin_user_data = dict()
        client_application_data = dict()

        admin_user_data['name'] = data['name']
        admin_user_data['created_by'] = super_user_id
        admin_user_data['email'] = data['email']
        admin_user_data['password'] = data['password']
        admin_user_data['user_type'] = 'ADMIN'

        client_application_data['name'] = data['name']
        client_application_data['client_type'] = 'public'
        client_application_data['authorization_grant_type'] = 'password'

        user = User.objects.create(**admin_user_data)

        client_application_data['user_id'] = user.user_id

        application = Application.objects.create(**client_application_data)

        print(super_user_id)

        user.application = application
        user.created_by = User.objects.get(user_id=1)
        user.save()

        logger.debug('Client creation successful')
        logger.debug(f'Exit {__name__} module, '
                     f'{create_client.__name__} method')

        return {'app': ApplicationSerializer(application).data,
                'user': UserSerializer(user).data}
    except ValidationError as ve:
        message = list(ve.get_full_details().values())[0][0]['message']
        logger.error('Organization creation failure')
        logger.error(f'Exit {__name__} module, '
                     f'{create_client.__name__} method')
        raise CustomApiException(400, message)