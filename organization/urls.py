from django.urls import path

from organization import views

urlpatterns = [
    path('', views.create_organization, name='create_organization'),
    path('all', views.get_organizations, name='get_organizations'),
    path('<int:organization_id>', views.do_organization,
         name='do_organization'),
]
