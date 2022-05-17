"""This module contains serializers for all the models
"""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from credential.models import Component
from credential.models import Item
from credential.models import Vault
from credential.models import VaultAccess

from utils.encryption_decryption import encrypt, decrypt, generate_key


class ItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(required=False)

    class Meta:
        model = Item
        fields = ('item_id', 'item_uid', 'key', 'value', 'salt', 'active',
                  'component', 'organization',
                  'created_at', 'created_by', 'updated_at', 'updated_by')
        read_only_fields = ('component',)


class ComponentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, write_only=True)

    class Meta:
        model = Component
        fields = ('component_id', 'component_uid', 'name', 'description',
                  'active', 'organization', 'vault', 'items',
                  'created_at', 'created_by', 'updated_at', 'updated_by')

    # override create method for nested objects creation
    def create(self, validated_data):
        items = validated_data.pop('items')

        component = Component.objects.create(**validated_data)

        for item in items:
            salt = generate_key()
            item['value'] = encrypt(item.get('value'), salt)
            item['salt'] = salt.decode('utf-8')

            Item.objects.create(component=component, **item,
                                created_by=component.created_by,
                                organization=component.organization)

        return component

    # override update method to update nested objects
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.updated_by = validated_data.get('updated_by')

        instance.save()

        items = validated_data.pop('items')

        for item in items:
            item_id = item.get('item_id', None)

            if item_id:
                component_item = Item.objects.get(item_id=item_id,
                                                  component=instance)
                component_item.key = item.get('key', component_item.key)
                # component_item.value = item.get('value', component_item.value)
                component_item.active = \
                    item.get('active', component_item.active)
                component_item.updated_by = component_item.created_by
                component_item.organization = item \
                    .get('organization', component_item.organization)
                component_item.updated_by = validated_data['updated_by']
                component_item.save()
            else:
                salt = generate_key()
                item['value'] = encrypt(item.get('value'), salt)
                item['salt'] = salt.decode('utf-8')

                Item.objects.create(component=instance, **item,
                                    created_by=instance.created_by)

        return instance


class ComponentResponseSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Component
        fields = ('component_id', 'component_uid', 'name', 'description',
                  'active', 'organization', 'vault', 'items',
                  'created_at', 'created_by', 'updated_at', 'updated_by')


class ComponentOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('component_id', 'name', 'description',
                  'vault', 'organization', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by')


class VaultSerializer(serializers.ModelSerializer):
    components = ComponentOnlySerializer(many=True, read_only=True)

    class Meta:
        model = Vault
        fields = ('vault_id', 'vault_uid', 'name', 'description',
                  'organization', 'components', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by')

    # override update method
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.updated_by = validated_data.get('updated_by')
        instance.save()

        return instance


class VaultOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Vault
        fields = ('vault_id', 'vault_uid', 'name', 'description',
                  'organization', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by')


class VaultResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vault
        fields = ('vault_id', 'vault_uid', 'name', 'description',
                  'organization', 'active',)


class VaultAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultAccess
        fields = '__all__'

    # override update method for partial update
    def update(self, instance, validated_data):
        instance.scope = validated_data.get('scope', instance.scope)
        instance.access_level = validated_data.get('access_level',
                                                   instance.access_level)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
