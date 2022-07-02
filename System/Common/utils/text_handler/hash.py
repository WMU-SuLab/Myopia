# -*- encoding: utf-8 -*-
"""
@File Name      :   hash.py    
@Create Time    :   2022/4/22 12:26
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import json

from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
from django.conf import settings


def encrypt_by_cryptography(raw_str: str, secret_key: bytes or str) -> str:
    if not raw_str:
        return ''
    f = Fernet(secret_key)
    return f.encrypt(raw_str.encode(encoding='utf8')).decode('utf8')


def decrypt_by_cryptography(encrypt_str: str, secret_key: bytes or str) -> str:
    if not encrypt_str:
        return ''
    try:
        f = Fernet(secret_key)
        encrypt_bytes = bytes(encrypt_str, encoding='utf8')
        return f.decrypt(encrypt_bytes).decode(encoding='utf8')
    except InvalidToken or InvalidSignature:
        return ''


def encrypt_text(text: str) -> str:
    if not text:
        return ''
    return encrypt_by_cryptography(text, settings.CRYPTOGRAPHY_SECRET_KEY)


def decrypt_text(text: str) -> str:
    if not text:
        return ''
    return decrypt_by_cryptography(text, settings.CRYPTOGRAPHY_SECRET_KEY)


def encrypt_dict_to_text(data: dict) -> str:
    if not data:
        return ''
    return encrypt_by_cryptography(json.dumps(data), settings.CRYPTOGRAPHY_SECRET_KEY)


def decrypt_text_to_dict(text: str) -> dict:
    if not text:
        return {}
    return json.loads(decrypt_by_cryptography(text, settings.CRYPTOGRAPHY_SECRET_KEY))
