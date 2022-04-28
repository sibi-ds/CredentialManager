from django.urls import path, include

from organization import views

urlpatterns = [
    path('', views.create_organization, name='create_organization'),
    path('<int:organization_id>', views.do_organization,
         name='do_organization'),
    # path('users/<uuid:uid>/vaults/', include('credential.urls')),
    # path('employees/', include('employee.urls')),
    # path('projects/', include('project.urls')),
]
