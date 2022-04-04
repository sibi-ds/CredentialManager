"""This module contains serializers for all the models
"""
from rest_framework import serializers

from credential.models import Component
from credential.models import ComponentAccess
from credential.models import Employee
from credential.models import Item
from credential.models import Project
from credential.models import Vault
from credential.models import VaultAccess


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('employee_id', 'name', 'email_address')


class ProjectSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(required=False)

    class Meta:
        model = Item
        fields = ('item_id', 'key', 'value', 'component')
        read_only_fields = ('component', )


class ComponentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Component
        fields = ('component_id', 'name', 'description', 'access_level',
                  'vault', 'items')

    def create(self, validated_data):
        items = validated_data.pop('items')
        component = Component.objects.create(**validated_data)

        for item in items:
            Item.objects.create(component=component, **item)

        return component

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
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
                component_item.save()
            else:
                Item.objects.create(component=instance, **item)

        return instance


class VaultSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, read_only=True)
    email_address = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Vault
        fields = ('vault_id', 'name', 'description', 'access_level',
                  'project', 'email_address', 'password', 'components', )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.access_level = validated_data.get('access_level',
                                                   instance.access_level)
        instance.project = validated_data.get('project', instance.project)

        return instance


class VaultAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaultAccess
        fields = '__all__'


class ComponentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAccess
        fields = '__all__'
