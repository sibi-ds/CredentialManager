import json
import logging

import requests
from django.contrib.auth import authenticate
from django.http import HttpRequest
from oauth2_provider.models import AccessToken, Application
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
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


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    user = authenticate(username=request.data['username'],
                        password=request.data['password'])

    if user:
        token_obj = AccessToken.objects.filter(user=user)
        app_obj = Application.objects.filter(user=user)
        print(app_obj)

        print(app_obj[0].client_id)
        url = 'http://' + request.get_host() + '/auth/token/'
        payload = {
            "grant_type": "password",
            "username": request.data['username'],
            "password": request.data['password'],
            "client_id": app_obj[0].client_id,
            # "client_secret": app_obj[0].client_secret
        }
        token_obj = requests.post(url=url, data=payload)
        token_obj = json.loads(token_obj.text)
        print(">>>>>>>>>>>", token_obj.keys())
    else:
        return Response("not ok")

    return Response(token_obj)
