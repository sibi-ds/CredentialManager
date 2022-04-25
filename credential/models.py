"""This module contains all model classes
"""
from django.db import models
from django_cryptography.fields import encrypt

from employee.models import EmployeeAccount
from project.models import Project


# all models subclasses the base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# model to define access level for a vault and component
class AccessLevel(BaseModel):
    access_id = models.AutoField(primary_key=True)
    access_level = models.CharField(max_length=45, unique=True)


# model to define vault for a user
class Vault(BaseModel):
    vault_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    employee = models.ForeignKey(EmployeeAccount, to_field='email',
                                 related_name='vaults', db_column='email',
                                 on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    description = models.TextField()
    access_level = models.ForeignKey(AccessLevel, to_field='access_level',
                                     db_column='access_level',
                                     related_name='vault',
                                     on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True,
                                on_delete=models.CASCADE,
                                to_field='project_id',
                                related_name='vaults')


# model to define component of a vault
class Component(BaseModel):
    component_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.TextField()
    access_level = models.ForeignKey(AccessLevel, to_field='access_level',
                                     db_column='access_level',
                                     related_name='component',
                                     on_delete=models.CASCADE)
    vault = models.ForeignKey(Vault, to_field='vault_id',
                              on_delete=models.CASCADE,
                              related_name='components')


# model to define item of a component
class Item(BaseModel):
    item_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=45)
    value = encrypt(models.CharField(max_length=45))
    component = models.ForeignKey(Component, on_delete=models.CASCADE,
                                  to_field='component_id',
                                  related_name='items')


# model to define vault access for a user
class VaultAccess(BaseModel):
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeAccount, to_field='email',
                                 db_column='email',
                                 on_delete=models.CASCADE)


# model to define component access for a user
class ComponentAccess(BaseModel):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeAccount, to_field='email',
                                 db_column='email',
                                 on_delete=models.CASCADE)
