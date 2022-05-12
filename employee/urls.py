from django.urls import path

from employee import views

urlpatterns = [
    path('new', views.create_employee, name='create_employee'),
    path('', views.create_employees, name='create_employees'),
    path('login', views.get_employee, name='get_employee'),
    path('all', views.get_employees, name='get_employees'),
    # path('<uuid:uid>', views.update_employee, name='update_employee'),
    path('check', views.check, name='check')
    # path('register', views.create_employee, name='register'),
    # path('login', views.login, name='login'),
    # path('sample', views.sample, name='sample'),
]
