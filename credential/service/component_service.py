from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from rest_framework.response import Response

from credential.models import Component
from credential.models import Item

from credential.serializer import ComponentSerializer
from credential.serializer import ItemSerializer


def create_component(project_id, vault_id, data):
    try:
        with transaction.atomic():
            items_dictionary = data.pop('items')
            print(data, items_dictionary)
            # component = Component.objects.create(**data, vault_id=vault_id)
            # items = [Item(**item, component=component) for item in items_dictionary]
            # items = Item.objects.bulk_create(items)

            component = Component.objects.get(component_id=3)
            # items = Item.objects.filter(component_id=3)

            serializer = ComponentSerializer(component)
            print(serializer)
            # serializer.is_valid()
            print(serializer.data)
            return Response(serializer.data)
    except DatabaseError:
        pass

    return serialize(component)


def get_component(project_id, vault_id, component_id, data):
    try:
        component = Component.objects.get(vault_id=vault_id,
                                          component_id=component_id)

        return serialize(component)
    except ObjectDoesNotExist:
        return Response('No such component exist')


def update_component(project_id, vault_id, component_id, data):
    component = Component(**data, project_id=project_id)
    component.save()
    return serialize(component)


def serialize(data):
    serializer = ComponentSerializer(data)
    return Response(serializer.data)
