from django.urls import path

from client import views

urlpatterns = [
    path('', views.create_client, name='create_client'),
    path('get', views.get_client, name='get_client'),
]
