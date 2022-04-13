"""This module contains serializers related to employee information
"""
from rest_framework import serializers

from employee.models import EmployeeAccount


class EmployeeAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeAccount
        fields = ['id', 'name', 'email', ]
