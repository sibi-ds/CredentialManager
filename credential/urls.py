from django.urls import path

from . import views

urlpatterns = [
    path('<int:project_id>/vaults', views.create_vault,
         name='create_vault'),
    path('<int:project_id>/vaults/<int:vault_id>', views.do_vault,
         name='do_vault'),
    path('<int:project_id>/vaults/<int:vault_id>/components',
         views.create_component, name='create_component'),
    path('<int:project_id>/vaults/<int:vault_id>/components/<int:component_id>',
         views.do_component, name='do_component'),
    path('<int:project_id>/vaults/<int:vault_id>/components/<int:component_id>/accesses',
         views.do_access, name='do_access'),
]
