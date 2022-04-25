from django.urls import path

from project import views

urlpatterns = [
    path('', views.create_project, name='create_project'),
]
