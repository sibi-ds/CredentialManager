"""This module is used to validate the fields
"""
from django.core.validators import RegexValidator


class Validator:
    """Regex Validators
    """

    ORGANIZATION_NAME_REGEX = RegexValidator(
        r'^[a-zA-Z0-9 \'\.-]{4,45}$', 'Enter a valid organization name'
    )

    EMPLOYEE_NAME_REGEX = RegexValidator(
        r'^[a-zA-Z \.\']{4,70}$', 'Enter a valid employee name'
    )

    PROJECT_NAME_REGEX = RegexValidator(
        r'^[a-zA-Z \.\']{4,45}$', 'Enter a valid project name'
    )

    VAULT_NAME_REGEX = RegexValidator(
        r'^[a-zA-Z \.\']{4,45}$', 'Enter a valid vault name'
    )

    COMPONENT_NAME_REGEX = RegexValidator(
        r'^[a-zA-Z \.\']{4,45}$', 'Enter a valid component name'
    )

    PASSWORD_REGEX = RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-])'
        r'[A-Za-z\d@$!#%*?&-]{8,32}$',
        'Enter valid password')
