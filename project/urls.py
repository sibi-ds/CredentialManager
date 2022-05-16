from django.urls import path

from project import views

urlpatterns = [
    path('', views.create_projects, name='create_projects'),
    path('new', views.create_project, name='create_project'),
    path('all', views.get_projects, name='get_projects'),
    path('<uuid:project_uid>', views.get_project, name='get_project'),
    path('<uuid:project_uid>/assign_employee', views.assign_employee,
         name='assign_employee'),
]
