from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from credential.models import Employee
from credential.models import UserAccess
from credential.models import Vault

from credential.serializer import UserAccessSerializer


def create_user_access(project_id, vault_id, component_id, data):
    try:
        employee_email_address = data.get('email_address')
        employee = Employee.objects.get(project_id=project_id,
                                        email_address=employee_email_address)

        user_access = UserAccess.objects.create(
            employee_id=employee_email_address,
            component_id=component_id
        )
    except ObjectDoesNotExist:
        return Response('User not belongs to the project')

    return serialize(user_access)


def remove_user_access(project_id, vault_id, component_id, data):
    employee_email_address = data.get('email_address')
    user_access = UserAccess.objects.get(
        employee_id=employee_email_address,
        component_id=component_id
    )
    user_access.delete()
    return Response('The access for ' + employee_email_address + 'is removed')


def serialize(data):
    serializer = UserAccessSerializer(data)
    return Response(serializer.data)
