from oauth2_provider.models import AbstractApplication


class Client(AbstractApplication):
    class Meta:
        db_table = 'cm_client'
