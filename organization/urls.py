from django.urls import path, include

from organization import views

urlpatterns = [
    path('create', views.create_organization, name='create_organization'),
    path('', views.get_organizations, name='get_organizations'),
    path('<int:organization_id>', views.do_organization,
         name='do_organization'),
]
