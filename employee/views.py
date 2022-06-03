"""this module is used to do employee related operations
"""
import logging

from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest

from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.service import employee_service

from files import file_reader

from organization.models import Organization

from utils.api_exceptions import CustomApiException


logger = logging.getLogger('credential-manager-logger')


@api_view(['POST', ])
def create_employee(request: HttpRequest):
    """used to create employee in an organization
    """
    try:
        logger.debug(f'Enter {__name__} module, create_employee method')
        organization_id = request.query_params.get('organization_id')
        employee = employee_service.create_employee(organization_id,
                                                    request.data)
        logger.debug(f'Exit {__name__} module, create_employee method')
        return Response(employee)
    except CustomApiException as e:
        logger.error(f'Exit {__name__} module, create_employee method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET'])
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
            employee['created_by'] = organization.organization_id

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


@api_view(['GET'])
@transaction.atomic
def get_employee(request: HttpRequest):
    """used to get employee details and associated vaults using employee email
    """
    try:
        logger.debug(f'Enter {__name__} module, get_employee method')
        organization_id = request.query_params.get('organization_id')
        employee = employee_service.get_employee(organization_id, request.data)
        logger.debug(f'Exit {__name__} module, get_employee method')
        return Response(employee)
    except CustomApiException as e:
        logger.error('Load valid details in the file. '
                     'Employees creation failure')
        logger.error(f'Exit {__name__} module, get_employee method')
        raise CustomApiException(e.status_code, e.detail)


@api_view(['GET'])
def get_employees(request: HttpRequest):
    """used to get all vaults from an organization
    """
    logger.info(f'Enter {__name__} module, {get_employees.__name__} method')

    try:
        organization_id = request.query_params.get('organization_id')
        employee_serializer = employee_service.get_employees(
            organization_id, request.data
        )
        return Response(employee_serializer)
    except KeyError:
        logger.error('Enter valid details')
        logger.error(f'Exit {__name__} module, '
                     f'{get_employees.__name__} method')
        raise CustomApiException(400, 'Enter valid details')
    except Organization.DoesNotExist:
        logger.error('No such organization exist')
        logger.error(f'Exit {__name__} module, '
                     f'{get_employees.__name__} method')
        raise CustomApiException(404, 'No such organization exist')


@api_view(['PUT', 'PATCH'])
def do_employee(request: HttpRequest, employee_uid):
    organization_id = request.query_params.get('organization_id')

    if request.method == 'PUT':
        """used to update employee details
        """
        try:
            employee_serializer = employee_service.update_employee(
                organization_id, employee_uid, request.data
            )
            logger.debug(f'Exit {__name__} module, do_employee method')
            return Response(employee_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_employee method')
            raise CustomApiException(e.status_code, e.detail)

    if request.method == 'PATCH':
        """used to update employee status
        """
        try:
            employee_serializer = employee_service.update_employee_status(
                organization_id, employee_uid, request.data
            )
            logger.debug(f'Exit {__name__} module, do_employee method')
            return Response(employee_serializer)
        except CustomApiException as e:
            logger.error(f'Exit {__name__} module, do_employee method')
            raise CustomApiException(e.status_code, e.detail)


@api_view(['GET'])
def generate_token(request: HttpRequest):
    pass


@api_view(['GET'])
def logout(request: HttpRequest):
    pass


@api_view(['GET'])
def get(request: HttpRequest):
    employees = Employee.objects.all()
    return Response(EmployeeSerializer(employees, many=True).data)
