"""This module is used to validate the fields
"""
from django.core.validators import RegexValidator


class Validator:
    """Regex Validators
    """

    ORGANIZATION_NAME_REGEX = RegexValidator(
        r'^(?=.{4,45}$)[a-zA-Z0-9]+([-.@ \']?[a-zA-Z0-9]+)*$',
        'Enter a valid organization name length between 4 and 45 characters'
    )

    EMPLOYEE_NAME_REGEX = RegexValidator(
        r'^(?=.{4,70}$)\s*([A-Za-z]{1,}([\.,] |[-\']| ))+[A-Za-z]+\.?\s*$',
        'Enter a valid employee full name length between 4 and 45 characters'
    )

    PROJECT_NAME_REGEX = RegexValidator(
        r'^(?=.{4,45}$)[a-zA-Z0-9]+([-.@ \']?[a-zA-Z0-9]+)*$',
        'Enter a valid project name length between 4 and 45 characters'
    )

    VAULT_NAME_REGEX = RegexValidator(
        r'^(?=.{4,45}$)[a-zA-Z0-9]+([-.@ \']?[a-zA-Z0-9]+)*$',
        'Enter a valid vault name length between 4 and 45 characters'
    )

    COMPONENT_NAME_REGEX = RegexValidator(
        r'^(?=.{4,45}$)[a-zA-Z0-9]+([-.@ \']?[a-zA-Z0-9]+)*$',
        'Enter a valid component name length between 4 and 45 characters'
    )

    PASSWORD_REGEX = RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-])'
        r'[A-Za-z\d@$!#%*?&-]{8,32}$',
        'Enter a valid password length between 8 and 32 characters'
    )

    VALUE_LENGTH_REGEX = RegexValidator(
        r'^[a-zA-Z0-9-_=]{44,88}$',
        'Enter a valid value length can up to 32 characters'
    )

    KEY_LENGTH_REGEX = RegexValidator(
        r'^[a-zA-Z0-9-_=]{4,45}$',
        'Enter key length between 4 to 44 characters'
    )
