"""used to encrypt and decrypt a string using salt
"""
import os

from cryptography.fernet import Fernet
import base64
import logging
import traceback


logger = logging.getLogger('credential-manager-logger')


def encrypt(pas, salt):
    """used to encrypt given value with salt
    """
    try:
        pas = str(pas)
        cipher_pass = Fernet(salt)
        encrypt_pass = cipher_pass.encrypt(pas.encode('ascii'))
        encrypt_pass = base64.urlsafe_b64encode(encrypt_pass).decode("ascii")
        return encrypt_pass
    except Exception as e:
        logger.error(traceback.format_exc())
        return None


def decrypt(pas, salt):
    """used to decrypt given value with salt
    """
    try:
        pas = base64.urlsafe_b64decode(pas)
        cipher_pass = Fernet(salt)
        decode_pass = cipher_pass.decrypt(pas).decode("ascii")
        return decode_pass
    except Exception as e:
        logger.error(traceback.format_exc())
        return None


def generate_key():
    """used to generate random salt value
    """
    return base64.urlsafe_b64encode(os.urandom(32))
