"""This module is used to implement AES-256 encryption and decryption
"""
import base64
import logging
from secrets import token_bytes

from Crypto import Random
from Crypto.Cipher import AES

from utils.api_exceptions import CustomApiException

logger = logging.getLogger('credential-manager-logger')


def pad(s):
    """add padding to match the block size of 16 bytes
    """
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)


def encrypt(message):
    """encrypt the given message with the 256 bits key
    """
    try:
        logger.debug(f'Enter {__name__} module, {encrypt.__name__} method')
        key = token_bytes(32)
        message = pad(message.encode())
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encoded = iv + cipher.encrypt(message)
        encoded_text = base64.urlsafe_b64encode(encoded).decode()
        texted_key = base64.urlsafe_b64encode(key).decode()
        logger.debug('Encode successful')
        logger.debug(f'Exit {__name__} module, {encrypt.__name__} method')
        return {'encoded_text': encoded_text, 'texted_key': texted_key}
    except Exception as e:
        logger.error(e)
        logger.error('Encode failure')
        logger.error(f'Exit {__name__} module, {encrypt.__name__} method')
        return None


def decrypt(encoded_text, texted_key):
    """decrypt the given message with the 256 bits key
    """
    try:
        logger.debug(f'Enter {__name__} module, {decrypt.__name__} method')
        encoded = base64.urlsafe_b64decode(encoded_text)
        key = base64.urlsafe_b64decode(texted_key)
        iv = encoded[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decoded = cipher.decrypt(encoded[AES.block_size:])
        message = decoded.rstrip(b'\0').decode()
        logger.debug('Decode successful')
        logger.debug(f'Exit {__name__} module, {decrypt.__name__} method')
        return message
    except Exception as e:
        logger.error(e)
        logger.error('Decode failure')
        logger.error(f'Exit {__name__} module, {decrypt.__name__} method')
        return None
