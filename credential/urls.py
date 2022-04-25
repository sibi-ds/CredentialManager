from django.urls import path

from credential import views


urlpatterns = [
    path('', views.create_vault, name='create_vault'),
    path('<int:vault_id>', views.do_vault, name='do_vault'),
    path('<int:vault_id>/components', views.create_component,
         name='create_component'),
    path('<int:vault_id>/components/<int:component_id>',
         views.do_component, name='do_component'),
    path('<int:vault_id>/accesses', views.do_vault_access,
         name='do_vault_access'),
    path('<int:vault_id>/components/<int:component_id>/accesses',
         views.do_component_access, name='do_component_access'),
]
