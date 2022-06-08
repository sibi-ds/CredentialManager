"""this module contains employee models
"""
import uuid

from django.db import models

from organization.models import Organization

from project.models import Project

from utils.validators import Validator


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class Employee(BaseModel):

    class Meta:
        db_table = 'cm_employee'

    employee_id = models.AutoField(primary_key=True)
    employee_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                    unique=True)
    name = models.CharField(max_length=70, null=False,
                            validators=[Validator.EMPLOYEE_NAME_REGEX])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    organization = models.ForeignKey(Organization, to_field='organization_id',
                                     related_name='employees',
                                     db_column='organization_id',
                                     on_delete=models.CASCADE)

    projects = models.ManyToManyField(Project,
                                      related_name='employees',
                                      blank=True)

    created_by = models.ForeignKey(Organization, to_field='organization_id',
                                   db_column='created_by',
                                   related_name='created_employees',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.email
