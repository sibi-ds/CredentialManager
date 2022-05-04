"""this module used to create employees and projects
using csv files
"""
import csv
import logging

from pathlib import Path

from CredentialManager import settings


logger = logging.getLogger('credential-manager-logger')


def create_employees():
    """Read employees.txt file as csv and convert
    into the list of employee dictionary
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_employees.__name__} method')

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

    logger.debug(f'Exit {__name__} module, '
                 f'{create_employees.__name__} method')

    return employees


def create_projects():
    """Read projects.txt file as csv and convert
    into the list of project dictionary
    """
    logger.debug(f'Enter {__name__} module, '
                 f'{create_projects.__name__} method')

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

    logger.debug(f'Exit {__name__} module, '
                 f'{create_projects.__name__} method')

    return projects
