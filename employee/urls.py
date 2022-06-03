from django.urls import path

from employee import views

urlpatterns = [
    path('new', views.create_employee, name='create_employee'),
    path('', views.create_employees, name='create_employees'),
    path('login', views.get_employee, name='get_employee'),
    path('all', views.get_employees, name='get_employees'),
    path('<uuid:employee_uid>', views.do_employee,
         name='do_employee'),

    path('get', views.get, name='get'),
]
