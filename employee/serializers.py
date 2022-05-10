"""This module contains serializers related to employee information
"""
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from credential.serializers import VaultResponseSerializer

from employee.models import Employee


# class EmployeeAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeAccount
#         fields = ['employee_id', 'name', 'email', 'is_active',
#                   'created_at', 'created_by', 'updated_at', 'updated_by', ]
#
#     # override create method for hashing password of an employee
#     def create(self, validated_data):
#         name = validated_data.get('name')
#         email = validated_data.get('email')
#
#         employee = EmployeeAccount.objects.create(name=name, email=email,
#                                                   is_active=True)
#
#         employee.password = make_password(validated_data.get('password'))
#         employee.save()
#
#         return employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_uid', 'name', 'email',
                  'organization', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by', ]

    # override create method for hashing password of an employee
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')
        organization = validated_data.get('organization')
        created_by = validated_data.get('created_by')

        employee = Employee.objects.create(
            name=name, email=email, organization=organization,
            created_by=created_by
        )

        employee.password = make_password(validated_data.get('password'))
        employee.save()

        return employee


class EmployeeResponseSerializer(serializers.ModelSerializer):

    created_vaults = VaultResponseSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_uid', 'name', 'email',
                  'organization', 'active',
                  'created_vaults',
                  'created_at', 'created_by', 'updated_at', 'updated_by', ]
