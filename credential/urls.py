from django.urls import path

from credential import views


urlpatterns = [
    path('', views.create_vault, name='create_vault'),
    path('all', views.get_vaults, name='get_vaults'),
    path('<int:vault_id>', views.do_vault, name='do_vault'),
    path('<int:vault_id>/component', views.create_component,
         name='create_component'),
    path('<int:vault_id>/component/<int:component_id>',
         views.do_component, name='do_component'),
    path('<int:vault_id>/access', views.create_vault_access,
         name='create_vault_access'),
    path('<int:vault_id>/access/<int:vault_access_id>', views.do_vault_access,
         name='do_vault_access'),
]
