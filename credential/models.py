"""This module contains all model classes
"""
from django.db import models
from django_cryptography.fields import encrypt


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Project(BaseModel):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email_address = models.EmailField(max_length=45, unique=True)
    description = models.TextField()


class Employee(BaseModel):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email_address = models.EmailField(max_length=45, unique=True)
    projects = models.ManyToManyField(Project, related_name='employees',
                                      blank=True)


class AccessLevel(BaseModel):
    access_id = models.AutoField(primary_key=True)
    access_level = models.CharField(max_length=45, unique=True)


class Vault(BaseModel):
    vault_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email_address = models.EmailField(max_length=45)
    password = encrypt(models.CharField(max_length=45))
    description = models.TextField()
    access_level = models.ForeignKey(AccessLevel, to_field='access_level',
                                     db_column='access_level',
                                     related_name='vault',
                                     on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=True, null=True,
                                on_delete=models.CASCADE,
                                to_field='project_id',
                                related_name='vaults')


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


class Item(BaseModel):
    item_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=45)
    value = encrypt(models.CharField(max_length=45))
    component = models.ForeignKey(Component, on_delete=models.CASCADE,
                                  to_field='component_id',
                                  related_name='items')


class VaultAccess(BaseModel):

    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, to_field='email_address',
                                 db_column='email_address',
                                 on_delete=models.CASCADE)


class ComponentAccess(BaseModel):

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, to_field='email_address',
                                 db_column='email_address',
                                 on_delete=models.CASCADE)
