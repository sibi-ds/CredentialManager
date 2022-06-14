import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from oauth2_provider.models import Application

from client.models import Client
from organization.models import Organization

from project.models import Project

from user.custom_user import UserManager

from utils.validators import Validator


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """model to define employee details
    which is used as the django auth user model
    """
    class Meta:
        db_table = 'cm_user'

    user_id = models.AutoField(primary_key=True)
    user_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                unique=True)
    name = models.CharField(max_length=70, null=False)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    user_types = [
        ("SUPER_USER", "SUPER_USER"),
        ("CLIENT", "CLIENT"),
        ("EMPLOYEE", "EMPLOYEE"),
    ]

    user_type = models.CharField(choices=user_types, max_length=20, null=False)

    application = models.ForeignKey(Application, to_field='id',
                                    related_name='client_users',
                                    on_delete=models.CASCADE,
                                    null=True)

    projects = models.ManyToManyField(Project,
                                      related_name='mapped_employees',
                                      blank=True)

    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE,
                                   db_column='created_by',
                                   related_name='created_users',
                                   null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.email

    objects = UserManager()
