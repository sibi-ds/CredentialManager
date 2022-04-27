from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# model to define tenant
class Organization(BaseModel):
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
