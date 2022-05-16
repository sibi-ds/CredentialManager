"""This module contains serializers related to project information
"""
from rest_framework import serializers

from credential.serializers import VaultSerializer
# from employee.serializers import EmployeeAccountSerializer
from employee.serializers import EmployeeSerializer

from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    vaults = VaultSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('project_id', 'project_uid', 'name', 'email', 'description',
                  'organization', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by')
