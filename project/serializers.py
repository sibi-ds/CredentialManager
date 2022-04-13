"""This module contains serializers related to project information
"""
from rest_framework import serializers

from credential.serializers import VaultSerializer
from employee.serializers import EmployeeAccountSerializer
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    employees = EmployeeAccountSerializer(many=True, read_only=True)
    vaults = VaultSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
