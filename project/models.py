"""this module contains model for project details
"""
from django.db import models

from organization.models import Organization


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Project(BaseModel):

    class Meta:
        db_table = 'cm_project'

    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, unique=True)
    description = models.TextField()

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     to_field='organization_id',
                                     db_column='organization_id',
                                     related_name='projects')
