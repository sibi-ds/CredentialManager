from django.urls import path

from . import views

urlpatterns = [
    path('vaults', views.create_vault, name='create_vault'),
    path('vaults/<int:vault_id>', views.do_vault, name='do_vault'),
    path('vaults/<int:vault_id>/components', views.create_component,
         name='create_component'),
    path('vaults/<int:vault_id>/components/<int:component_id>',
         views.do_component, name='do_component'),
    path('vaults/<int:vault_id>/accesses', views.do_vault_access,
         name='do_vault_access'),
    path('vaults/<int:vault_id>/components/<int:component_id>/accesses',
         views.do_component_access, name='do_component_access'),
    path('', views.get, name='get'),
]
