import csv
from pathlib import Path

from CredentialManager import settings
# from employee.models import EmployeeAccount
from employee.models import Employee
from project.models import Project


def create_employees():
    print(Path(str(settings.BASE_DIR) + '\\files\\' + 'employees.txt'))
    employees = list()

    with open(Path(str(settings.BASE_DIR) + '\\files\\' + 'employees.txt')) \
            as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                employee = dict(name=row[0], email=row[1],
                                password=row[2])

                employees.append(employee)
                line_count += 1

    return employees


def create_projects():
    projects = list()

    with open(Path(str(settings.BASE_DIR) + '\\files\\' + 'projects.txt')) \
            as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                project = dict(name=row[0], email=row[1],
                               description=row[2])
                projects.append(project)
                line_count += 1

    return projects
