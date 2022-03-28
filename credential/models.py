"""This module contains classes
which are used to store credentials
and store user access details
"""
from django.db import models


class Credential(models.Model):
    credential_id = models.AutoField(primary_key=True)
    access_level_id = models.IntegerField()
    name = models.CharField(max_length=45)
    description = models.TextField()


class CredentialDetails(models.Model):
    credential_details_id = models.AutoField(primary_key=True)
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    key = models.CharField(max_length=45)
    value = models.CharField(max_length=45)


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email_address = models.EmailField(max_length=45, unique=True)


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    email_address = models.EmailField(max_length=45, unique=True)


class AccessibleUser(models.Model):
    class Meta:
        unique_together = (('credential', 'employee'),)

    credential = models.ForeignKey(Credential,
                                   on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,
                                 to_field='email_address',
                                 db_column='email_address',
                                 on_delete=models.CASCADE)
