"""this module is used to do employee related operations
"""
import logging

from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from datetime import timedelta

from django.utils import timezone

# from employee.models import EmployeeAccount
# from employee.serializers import EmployeeAccountSerializer

from employee.models import Employee
from employee.serializers import EmployeeSerializer

from files import file_reader
from organization.models import Organization
from organization.views import is_valid_user

from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def create_employee(request):
#     """used to create employee
#     """
#     logger.info(f'Enter {__name__} module, create_employee method')
#     name = request.data.get("name")
#     email = request.data.get("email")
#     password = request.data.get("password")
#
#     if email is None or password is None or name is None:
#         logger.error('Employee creation failed')
#         raise CustomApiException(400,
#                                  'Please provide name, email and password')
#
#     employee = EmployeeAccount.objects.create_user(email, password, name)
#     employee_serializer = EmployeeAccountSerializer(employee)
#     logger.info(f'Exit {__name__} module, create_employee method')
#
#     return Response(employee_serializer.data)


# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def login(request):
#     username = request.data.get("email")
#     password = request.data.get("password")
#     if username is None or password is None:
#         return Response({'error': 'Please provide both username and password'},
#                         status=HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#
#     if not user:
#         return Response({'error': 'Invalid Credentials'},
#                         status=HTTP_404_NOT_FOUND)
#
#     token, _ = Token.objects.get_or_create(user=user)
#
#     seconds = request.data.get("seconds")
#
#     if is_token_expired(token, seconds):
#         token.delete()
#
#     token, _ = Token.objects.get_or_create(user=user)
#
#     return Response({'token': token.key, 'expires_in': expiring_in(token,
#                                                                    seconds)},
#                     status=HTTP_200_OK)


# def expiring_in(token, seconds):
#     """used to calculate the valid time left for a token
#     """
#     time_elapsed = timezone.now() - token.created
#     left_time = timedelta(seconds=seconds) - time_elapsed
#     return left_time


# def is_token_expired(token, seconds):
#     """used to determine whether a token is expired or not
#     """
#     return expiring_in(token, seconds) < timedelta(seconds=0)


# @csrf_exempt
# @api_view(["GET"])
# @permission_classes((IsAuthenticated,))
# def sample(request):
#     data = {'sample_data': 123}
#     return Response(data, status=HTTP_200_OK)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
# def token_expire_handler(token, seconds):
#     is_expired = is_token_expired(token, seconds)
#     if is_expired:
#         token.delete()
#         token = Token.objects.create(user=token.user)
#     return is_expired, token


@api_view(['POST', ])
def create_employees(request: HttpRequest):
    try:
        email = request.data.get("email")
        password = request.data.get('password')

        employee_datas = file_reader.create_employees()

        organization_id = request.query_params.get('organization_id')

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True
        )

        for employee in employee_datas:
            employee['organization'] = organization_id

        employee_list_serializer = EmployeeSerializer(
            data=employee_datas, many=True
        )

        employee_list_serializer.is_valid(raise_exception=True)
        employee_list_serializer.save()

        return Response(employee_list_serializer.data)
    except ValidationError:
        raise CustomApiException(400, 'Load valid details in the file')
    except KeyError:
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        raise CustomApiException(404, 'No such organization exist')
