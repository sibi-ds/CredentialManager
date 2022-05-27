"""this module contains model for project details
"""
import uuid

from django.db import models

from organization.models import Organization


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Project(BaseModel):

    class Meta:
        db_table = 'cm_project'

    project_id = models.AutoField(primary_key=True)
    project_uid = models.UUIDField(default=uuid.uuid4, editable=False,
                                   unique=True)
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45, unique=True)
    description = models.TextField()

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     to_field='organization_id',
                                     db_column='organization_id',
                                     related_name='projects')

    created_by = models.ForeignKey(Organization, to_field='organization_id',
                                   db_column='created_by',
                                   related_name='created_projects',
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name
