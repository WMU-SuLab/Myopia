# -*- encoding: utf-8 -*-
"""
@File Name      :   validator.py    
@Create Time    :   2022/4/25 10:57
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

from django.core import validators

from Common.utils.text_handler.validator import validate_phone


# todo:使用redis存储验证码，并写一套键值对处理方法
def validate_verification_code(
        verification_code: str = None,
        username: str = None,
        email: str = None,
        phone: str = None):
    if not 4 <= len(verification_code) <= 6:
        return False
    if username and validators.validate_email(username):
        pass
    elif username and validate_phone(username):
        pass
    elif email and validators.validate_email(username):
        pass
    elif phone and validate_phone(username):
        pass
    else:
        return False
