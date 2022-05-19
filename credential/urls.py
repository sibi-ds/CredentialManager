from django.urls import path

from credential import views


urlpatterns = [
    path('', views.create_vault, name='create_vault'),
    path('all', views.get_vaults, name='get_vaults'),
    path('<uuid:vault_uid>', views.do_vault, name='do_vault'),
    path('<uuid:vault_uid>/component', views.create_component,
         name='create_component'),
    path('<uuid:vault_uid>/component/<uuid:component_uid>',
         views.do_component, name='do_component'),
    path('<uuid:vault_uid>/access', views.create_vault_access,
         name='create_vault_access'),
    path('<uuid:vault_uid>/access/remove', views.remove_vault_access,
         name='remove_vault_access'),
    path('<uuid:vault_uid>/component/<uuid:component_uid>/item/<uuid:item_uid>',
         views.decrypt_item, name='decrypt_item'),
    path('component/item/decrypt', views.decrypt, name='decrypt'),
]
