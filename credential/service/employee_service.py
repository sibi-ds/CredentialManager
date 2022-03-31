from django.core.exceptions import ObjectDoesNotExist

from credential.models import Employee


def is_organization_employee(email_address):
    try:
        employee = Employee.objects.get(email_address=email_address)
        return employee
    except ObjectDoesNotExist:
        return None


def is_project_employee(email_address, project_id):
    try:
        employee = Employee.objects.get(projects__project_id=project_id,
                                        email_address=email_address)
        return employee
    except ObjectDoesNotExist:
        return None
