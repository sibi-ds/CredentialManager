from django.urls import path

from employee import views

urlpatterns = [
    path('', views.create_employees, name='create_employees'),
    # path('register', views.create_employee, name='register'),
    # path('login', views.login, name='login'),
    # path('sample', views.sample, name='sample'),
]
