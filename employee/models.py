"""this module contains employee models
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser

from django.db import models

from employee.managers import EmployeeManager

from project.models import Project


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class EmployeeAccount(AbstractBaseUser, PermissionsMixin, BaseModel):
    """model to define employee details
    which is used as the django auth user model
    """
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    projects = models.ManyToManyField(Project,
                                      related_name='employees',
                                      blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = EmployeeManager()
