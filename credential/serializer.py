from rest_framework import serializers
from credential.models import Vault
from credential.models import Component
from credential.models import Item
from credential.models import UserAccess


class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('item_id', 'key', 'value', 'component_id')


class ComponentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Component
        fields = ('component_id', 'name', 'description', 'vault_id', 'items')


class ComponentDeSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Component
        fields = ('name', 'description', 'vault', 'items')

    def create(self, validated_data):
        items = validated_data.pop('items')
        component = Component.objects.create(**validated_data)

        for item in items:
            Item.objects.create(component_id=component.component_id, **item)

        return component

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data \
    #         .get('description', instance.description)
    #
    #     instance.save()
    #
    #     items = validated_data.get('items')
    #
    #     for item in items:
    #         item_id = item.get('item_id', None)
    #
    #         if item_id:
    #             component_item = Item.objects \
    #                 .get(item_id=item_id, component=instance)
    #             component_item.key = item.get('key', item.key)
    #             component_item.value = item.get('value', item.value)
    #             component_item.save()
    #         else:
    #             Item.objects.create(component=instance, **item)
    #
    #     return instance


class UserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccess
        fields = '__all__'
