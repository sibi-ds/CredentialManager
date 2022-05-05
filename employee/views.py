"""this module is used to do employee related operations
"""
import logging

from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from credential.models import VaultAccess
from credential.serializers import VaultResponseSerializer
from employee.models import Employee
from employee.serializers import EmployeeSerializer, EmployeeResponseSerializer

from files import file_reader

from organization.models import Organization

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST', ])
def create_employees(request: HttpRequest):
    """used to create employees using employees csv file
    """
    try:
        logger.debug(f'Enter {__name__} module, create_employees method')

        email = request.data.get("email")

        employee_datas = file_reader.create_employees()

        organization_id = request.query_params.get('organization_id')

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True,
            email=email
        )

        for employee in employee_datas:
            employee['organization'] = organization.organization_id

        employee_list_serializer = EmployeeSerializer(
            data=employee_datas, many=True
        )

        employee_list_serializer.is_valid(raise_exception=True)
        employee_list_serializer.save()

        logger.debug('Employees creation successful')
        logger.debug(f'Exit {__name__} module, create_employees method')

        return Response(employee_list_serializer.data)
    except ValidationError:
        logger.error('Load valid details in the file. '
                     'Employees creation failure')
        logger.error(f'Exit {__name__} module, create_employees method')
        raise CustomApiException(500, 'Load valid details in the file')
    except KeyError:
        logger.error('Enter valid details.Employees creation failure')
        logger.error(f'Exit {__name__} module, create_employees method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist.Employees creation failure')
        logger.error(f'Exit {__name__} module, create_employees method')
        raise CustomApiException(404, 'No such organization exist')


@api_view(['POST'])
def get_employee(request: HttpRequest):
    """used to get employee details and associated vaults using employee email
    """
    try:
        logger.debug(f'Enter {__name__} module, get_employee method')

        email = request.data.get("email")
        organization_id = request.query_params.get('organization_id')

        organization = Organization.objects.get(
            organization_id=organization_id,
            active=True,
        )

        employee = Employee.objects.get(
            email=email, active=True,
            organization=organization.organization_id,
            organization__active=True
        )

        organization_level_vaults_accesses = VaultAccess.objects.filter(
            access_level='ORGANIZATION',
            active=True,
            organization=organization_id,
            organization__active=True
        )
        project_level_vaults_accesses = VaultAccess.objects.filter(
            access_level='PROJECT',
            active=True,
            organization=organization_id,
            organization__active=True,
            project__employees__employee_id=employee.employee_id
        )

        organization_level_vaults = [
            organization_vault_access.vault
            for organization_vault_access in organization_level_vaults_accesses
        ]

        project_level_vaults = [
            project_vault_access.vault
            for project_vault_access in project_level_vaults_accesses
        ]

        employee_serializer = EmployeeResponseSerializer(employee)

        response_employee = employee_serializer.data
        response_employee['organization_vaults'] \
            = VaultResponseSerializer(organization_level_vaults, many=True) \
            .data
        response_employee['project_vaults'] \
            = VaultResponseSerializer(project_level_vaults, many=True) \
            .data

        logger.debug(f'Exit {__name__} module, get_employee method')

        return Response(response_employee)
    except ValidationError:
        logger.error('Load valid details in the file. '
                     'Employees creation failure')
        logger.error(f'Exit {__name__} module, get_employee method')
        raise CustomApiException(500, 'Load valid details in the file')
    except KeyError:
        logger.error('Enter valid details. Employees creation failure')
        logger.error(f'Exit {__name__} module, get_employee method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('Organization not exist')
        logger.error(f'Exit {__name__} module, get_employee method')
        raise CustomApiException(404, 'No such organization exist')
    except Employee.DoesNotExist:
        logger.error('Employee not exist')
        logger.error(f'Exit {__name__} module, get_employee method')
        raise CustomApiException(404, 'No such employee exist')


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
