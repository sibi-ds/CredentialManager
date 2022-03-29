from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import serializers

from credential.models import Vault
from credential.serializer import VaultSerializer


def create_vault(project_id, data):
    vault = Vault.objects.create(**data, project_id=project_id)
    return serialize(vault)


def get_vault(project_id, vault_id, data):
    try:
        vault = Vault.objects.get(vault_id=vault_id,
                                  project_id=project_id,
                                  email_address=data.get('email_address'),
                                  password=data.get('password'))
        return serialize(vault)
    except ObjectDoesNotExist:
        return Response('No such vault exist')


def update_vault(project_id, vault_id, data):
    vault = Vault(**data, project_id=project_id)
    vault.save()
    return serialize(vault)


def serialize(data):
    serializer = VaultSerializer(data)
    return Response(serializer.data)
