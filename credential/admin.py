from django.contrib import admin

from credential.models import Component
from credential.models import Item
from credential.models import Vault
from credential.models import VaultAccess


admin.site.register(Vault)
admin.site.register(Component)
admin.site.register(Item)
admin.site.register(VaultAccess)
