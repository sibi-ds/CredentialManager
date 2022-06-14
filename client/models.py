from django.db import models

from oauth2_provider.models import AbstractApplication, Application


class Client(AbstractApplication):

    class Meta:
        db_table = "cm_client"
