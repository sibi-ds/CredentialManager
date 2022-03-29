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
        exclude = ('component', )


class ComponentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Component
        fields = ('component_id', 'name', 'description', 'vault_id', 'items')


class UserAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccess
        fields = '__all__'
