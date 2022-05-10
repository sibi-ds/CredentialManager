from django.urls import path

from project import views

urlpatterns = [
    path('', views.create_projects, name='create_projects'),
    path('new', views.create_project, name='create_project'),
    path('all', views.get_projects, name='get_projects'),
]
