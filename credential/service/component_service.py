from django.core.exceptions import ObjectDoesNotExist

from django.db import DatabaseError
from django.db import transaction

from rest_framework.response import Response

from credential.models import Component, Item
from credential.models import UserAccess
from credential.models import Vault

from credential.serializer import ComponentDeSerializer
from credential.serializer import ComponentSerializer


def create_component(project_id, vault_id, data):
    try:
        data['vault'] = vault_id
        serializer = ComponentDeSerializer(data=data)

        print(serializer)
        serializer.is_valid()
        print(serializer.validate_empty_values(data=data))
        print(serializer.errors)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response('Enter valid details')
    except Exception as ex:
        print(ex)
        return Response('Try after sometime')


def get_component(project_id, vault_id, component_id, data):
    try:
        email_address = data.get('email_address')
        vault = Vault.objects.get(vault_id=vault_id)

        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id)

        if vault.email_address == email_address:
            return serialize(component)

        user_access = UserAccess.objects.get(component_id=component_id,
                                             employee_id=email_address)

        return serialize(component)
    except ObjectDoesNotExist:
        return Response('You don\'t have access for this')


def update_component(project_id, vault_id, component_id, data):
    component = Component.objects.get(component_id=component_id)
    serializer = ComponentDeSerializer(instance=component, data=data)

    if serializer.is_valid():
        component = serializer.save()

    return serialize(component)


def serialize(data):
    serializer = ComponentSerializer(data)
    return Response(serializer.data)
