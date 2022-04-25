"""This module contains serializers for all the models
"""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from credential.models import AccessLevel
from credential.models import Component
from credential.models import ComponentAccess
from credential.models import Item
from credential.models import Vault
from credential.models import VaultAccess


class AccessLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessLevel
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(required=False)

    class Meta:
        model = Item
        fields = ('item_id', 'key', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by',
                  'value', 'component')
        read_only_fields = ('component', )


class ComponentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Component
        fields = ('component_id', 'name', 'description', 'access_level',
                  'active', 'created_at', 'created_by', 'updated_at',
                  'updated_by', 'vault', 'items')

    # override create method for nested objects creation
    def create(self, validated_data):
        items = validated_data.pop('items')
        component = Component.objects.create(**validated_data)

        for item in items:
            Item.objects.create(component=component, **item)

        return component

    # override update method to update nested objects
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.access_level = validated_data.get('access_level',
                                                   instance.access_level)
        instance.description = validated_data.get('description',
                                                  instance.description)

        instance.save()

        items = validated_data.pop('items')

        for item in items:
            item_id = item.get('item_id', None)

            if item_id:
                component_item = Item.objects.get(item_id=item_id,
                                                  component=instance)
                component_item.key = item.get('key', component_item.key)
                component_item.value = item.get('value', component_item.value)
                component_item.active = \
                    item.get('active', component_item.active)
                component_item.save()
            else:
                Item.objects.create(component=instance, **item)

        return instance


class ComponentOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('component_id', 'name', 'description', 'access_level',
                  'active', 'created_at', 'created_by', 'updated_at',
                  'updated_by')


class VaultSerializer(serializers.ModelSerializer):
    components = ComponentOnlySerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Vault
        fields = ('vault_id', 'name', 'description', 'access_level', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by',
                  'project', 'employee', 'password', 'components')

    # override create method for hashing password of a vault
    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        access_level = validated_data.get('access_level')
        project = validated_data.get('project', None)
        employee = validated_data.get('employee')
        vault = Vault.objects.create(name=name, description=description,
                                     access_level=access_level, active=True,
                                     employee=employee, project=project)
        vault.password = make_password(validated_data.get('password'))
        vault.save()

        return vault

    # override update method
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.access_level = validated_data.get('access_level',
                                                   instance.access_level)
        instance.project = validated_data.get('project', instance.project)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class VaultAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultAccess
        fields = '__all__'

    # override update method for partial update
    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class ComponentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAccess
        fields = '__all__'

    # override update method for partial update
    def update(self, instance, validated_data):
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
