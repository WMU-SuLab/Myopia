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

from cryptography.fernet import Fernet


def encrypt_by_cryptography(raw_str: str, secret_key: bytes or str)->bytes:
    f = Fernet(secret_key)
    return f.encrypt(raw_str.encode(encoding='utf8'))


def decrypt_by_cryptography(encrypt_str: str, secret_key: bytes or str)->str:
    f = Fernet(secret_key)
    encrypt_bytes = bytes(encrypt_str, encoding='utf8')
    return f.decrypt(encrypt_bytes).decode(encoding='utf8')
