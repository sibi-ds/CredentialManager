"""This module contains all model classes
"""
import uuid

from django.db import models

# from employee.models import EmployeeAccount
from employee.models import Employee

from organization.models import Organization

from project.models import Project

from utils.validators import Validator


# all models subclasses the base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# model to define vault for a user
class Vault(BaseModel):

    class Meta:
        db_table = 'cm_vault'

    vault_id = models.AutoField(primary_key=True)
    vault_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                 unique=True)
    name = models.CharField(max_length=45,
                            validators=[Validator.VAULT_NAME_REGEX])
    description = models.TextField()

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     to_field='organization_id',
                                     related_name='vaults')

    created_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='created_by',
                                   related_name='created_vaults',
                                   null=True)

    updated_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='updated_by',
                                   related_name='updated_vaults',
                                   null=True)

    def __str__(self):
        return self.name


# model to define component of a vault
class Component(BaseModel):

    class Meta:
        db_table = 'cm_component'

    component_id = models.AutoField(primary_key=True)
    component_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                     unique=True)
    name = models.CharField(max_length=45,
                            validators=[Validator.COMPONENT_NAME_REGEX])
    description = models.TextField()

    vault = models.ForeignKey(Vault, to_field='vault_id',
                              on_delete=models.CASCADE,
                              related_name='components')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     to_field='organization_id',
                                     db_column='organization_id')

    created_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='created_by',
                                   related_name='created_vault_components',
                                   null=True)

    updated_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='updated_by',
                                   related_name='updated_vault_components',
                                   null=True)

    def __str__(self):
        return self.name


# model to define item of a component
class Item(BaseModel):

    class Meta:
        db_table = 'cm_item'

    item_id = models.AutoField(primary_key=True)
    item_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                unique=True)
    key = models.CharField(max_length=45,
                           validators=[Validator.KEY_LENGTH_REGEX])
    value = models.CharField(max_length=88,)
    salt = models.CharField(max_length=44)

    component = models.ForeignKey(Component, on_delete=models.CASCADE,
                                  to_field='component_id',
                                  related_name='items')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     to_field='organization_id',
                                     db_column='organization_id')

    created_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='created_by',
                                   related_name='created_component_items',
                                   null=True)

    updated_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='updated_by',
                                   related_name='updated_component_items',
                                   null=True)

    def __str__(self):
        return self.key


# model to define vault access for users or organization or project
class VaultAccess(BaseModel):

    class Meta:
        db_table = 'cm_vault_access'

    vault_access_id = models.AutoField(primary_key=True)
    vault_access_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                        unique=True)

    access_levels = [
        ("INDIVIDUAL", "INDIVIDUAL"),
        ("PROJECT", "PROJECT"),
        ("ORGANIZATION", "ORGANIZATION"),
    ]

    access_level = models.CharField(choices=access_levels, max_length=20)

    scopes = [
        ('READ', 'READ'),
        ('READ/WRITE', 'READ/WRITE'),
    ]

    scope = models.CharField(choices=scopes, default='READ', max_length=20)

    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)

    employee = models.ForeignKey(Employee, to_field='employee_id',
                                 db_column='employee_id',
                                 on_delete=models.CASCADE,
                                 related_name='vault_accesses',
                                 null=True)

    project = models.ForeignKey(Project, blank=True, null=True,
                                on_delete=models.CASCADE,
                                to_field='project_id', )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     to_field='organization_id',
                                     db_column='organization_id',
                                     null=True)

    created_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='created_by',
                                   related_name='created_vault_accesses',
                                   null=True)

    updated_by = models.ForeignKey(Employee, to_field='employee_id',
                                   on_delete=models.CASCADE,
                                   db_column='updated_by',
                                   related_name='updated_vault_accesses',
                                   null=True)
