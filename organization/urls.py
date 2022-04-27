from django.urls import path, include

from organization import views

urlpatterns = [
    path('', views.create_organization, name='create_organization'),
    path('<int:organization_id>', views.do_organization,
         name='do_organization'),
    path('<int:organization_id>/vaults/', include('credential.urls')),
    path('<int:organization_id>/employees/', include('employee.urls')),
    path('<int:organization_id>/projects/', include('project.urls')),
]
