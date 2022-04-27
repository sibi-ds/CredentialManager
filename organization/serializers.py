"""This module contains serializer for tenant model
"""
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from organization.models import Organization


# serializer for tenant
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('organization_id', 'name', 'email', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by')

    # override create method for hashing password of a tenant
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')

        organization = Organization.objects.create(name=name, email=email)

        organization.password = make_password(validated_data.get('password'))
        organization.save()

        return organization

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.active = validated_data.get('active', instance.active)

        instance.save()

        return instance
