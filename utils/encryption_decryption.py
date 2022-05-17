"""used to encrypt and decrypt a string using salt
"""
import os

import base64
import logging
import traceback

from cryptography.fernet import Fernet


logger = logging.getLogger('credential-manager-logger')


def encrypt(pas, salt):
    """used to encrypt given value with salt
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{encrypt.__name__} method')
        pas = str(pas)
        cipher_pass = Fernet(salt)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        logger.debug(f'Exit {__name__} module, '
                     f'{encrypt.__name__} method')
        return encrypt_pass
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f'Exit {__name__} module, '
                     f'{encrypt.__name__} method')
        return None


def decrypt(pas, salt):
    """used to decrypt given value with salt
    """
    try:
        logger.debug(f'Enter {__name__} module, '
                     f'{decrypt.__name__} method')
        pas = base64.urlsafe_b64decode(pas)
        cipher_pass = Fernet(salt)
        decode_pass = cipher_pass.decrypt(pas).decode("ascii")
        logger.debug(f'Exit {__name__} module, '
                     f'{decrypt.__name__} method')
        return decode_pass
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f'Exit {__name__} module, '
                     f'{decrypt.__name__} method')
        return None


def generate_key():
    """used to generate random 32 character byte code
    that can be used as salt value
    """
    return base64.urlsafe_b64encode(os.urandom(32))
