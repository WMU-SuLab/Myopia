# -*- encoding: utf-8 -*-
"""
@File Name      :   hash.py    
@Create Time    :   2022/4/22 12:36
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

from django.conf import settings

from Common.utils.text_handler.hash import encrypt_by_cryptography, decrypt_by_cryptography


def encrypt(text):
    return encrypt_by_cryptography(text, settings.CRYPTOGRAPHY_SECRET_KEY)


def decrypt(text):
    return decrypt_by_cryptography(text, settings.CRYPTOGRAPHY_SECRET_KEY)
