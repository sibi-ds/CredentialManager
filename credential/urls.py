from django.urls import path

from . import views

urlpatterns = [
    path('', views.do_credentials, name='do_credentials'),
    path('<int:credential_id>/users', views.do_credential_details,
         name='do_credential_details'),
]
