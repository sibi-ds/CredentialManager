"""This module is used for password validation purpose
"""
import re


def is_password_valid(password):
    """checks the  following condition conditions for a password:
    1) length of the password is between 8 and 32
    2) must contain a number
    3) must contain a special character
    4) must contain uppercase and lower case letter
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-])' \
              r'[A-Za-z\d@$!#%*?&-]{8,32}$'

    match = re.search(pattern, password)

    return match is not None
