from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import serializers

from credential.models import Vault, Project, Employee
from credential.serializer import VaultSerializer
from credential.service import user_access_service, employee_service


def create_vault(project_id, data):
    vault = Vault.objects.create(**data, project_id=project_id)
    return vault


def get_vault(project_id, vault_id, data):
    try:
        email_address = data.get('email_address')

        vault = Vault.objects.get(vault_id=vault_id, project_id=project_id)

        vault_access = user_access_service.get_vault_access(vault_id,
                                                            email_address)

        if vault.email_address == email_address:
            return vault
        elif vault_access is not None:
            return vault
        elif vault.access_level == 'ORGANIZATION' \
                and employee_service.is_organization_employee(email_address) \
                is not None:
            return vault
        elif vault.access_level == 'PROJECT' \
                and employee_service \
                .is_project_employee(email_address,project_id) is not None:
            return vault
        else:
            return None
    except ObjectDoesNotExist:
        return None


def update_vault(project_id, vault_id, data):
    vault = Vault(**data, project_id=project_id)
    vault.save()
    return vault


def serialize(data):
    serializer = VaultSerializer(data)
    return Response(serializer.data)
