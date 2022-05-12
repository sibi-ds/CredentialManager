from django.urls import path

from project import views

urlpatterns = [
    path('', views.create_projects, name='create_projects'),
    path('new', views.create_project, name='create_project'),
    path('all', views.get_projects, name='get_projects'),
    path('<int:project_id>', views.get_project, name='get_project'),
    path('<int:project_id>/assign_employee', views.assign_employee,
         name='assign_employee'),
]
