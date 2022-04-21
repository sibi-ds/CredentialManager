from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from datetime import timedelta
from django.utils import timezone

from employee.models import EmployeeAccount
from employee.serializers import EmployeeAccountSerializer
from utils.api_exceptions import CustomApiException


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def create_employee(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")

    if email is None or password is None or name is None:
        raise CustomApiException(400, 'Please provide name, email and password')

    employee = EmployeeAccount.objects.create_user(email, password, name)
    employee_serializer = EmployeeAccountSerializer(employee)

    return Response(employee_serializer.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'expires_in': expires_in(token)},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def sample(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)


# this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=10) - time_elapsed
    return left_time


# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)


# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token
