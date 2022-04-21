from django.contrib import admin

# Register your models here.
from employee.models import EmployeeAccount

admin.site.register(EmployeeAccount)
