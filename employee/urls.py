from django.urls import path

from employee import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('sample', views.sample, name='sample'),
]
