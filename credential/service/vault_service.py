from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import serializers

from credential.models import Vault, Project, Employee
from credential.serializer import VaultSerializer
from credential.service import user_access_service


def create_vault(project_id, data):
    vault = Vault.objects.create(**data, project_id=project_id)
    return vault


def get_vault(project_id, vault_id, data):
    try:
        email_address = data.get('email_address')

        vault = Vault.objects.filter(vault_id=vault_id, project_id=project_id)

        if len(vault) > 0:
            vault = vault[0]

            if vault.email_address == email_address:
                return vault
            else:
                vault_access = user_access_service \
                    .get_vault_access(vault_id, email_address)

                if vault_access is not None:
                    return vault
                elif vault.access_level == 'PROJECT':
                    project = Project.objects.get(project_id=project_id)

                    for employee in project.employees:
                        if employee.email_address == email_address:
                            return vault

                    return None
                elif vault.access_level == 'ORGANIZATION':
                    employees = Employee.objects \
                        .filter(email_address=email_address)

                    if len(employees) > 0:
                        return vault
                    else:
                        return None
        else:
            return None

        return vault
    except ObjectDoesNotExist:
        return None


def update_vault(project_id, vault_id, data):
    vault = Vault(**data, project_id=project_id)
    vault.save()
    return vault


def serialize(data):
    serializer = VaultSerializer(data)
    return Response(serializer.data)
