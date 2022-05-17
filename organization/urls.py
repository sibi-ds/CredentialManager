from django.urls import path

from organization import views

urlpatterns = [
    path('', views.create_organization, name='create_organization'),
    path('all', views.get_organizations, name='get_organizations'),
    path('<uuid:organization_uid>', views.do_organization,
         name='do_organization'),
]
