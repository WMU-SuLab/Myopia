# -*- encoding: utf-8 -*-
"""
@File Name      :   validator.py    
@Create Time    :   2022/6/9 16:30
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

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from Common.utils.text_handler.validator import validate_phone_number


# form表单需要的验证器

def region_phone_number_validator(phone_number):
    if not validate_phone_number(phone_number):
        raise ValidationError("手机号码格式不正确")


phone_number_validators = [
    region_phone_number_validator,
    # RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式不正确')
]

password_validators = [
    # 不需要大写
    RegexValidator(r'^(?=.*[a-z])(?=.*\d)[a-zA-Z\d]{6,32}$', '密码格式不正确', 'invalid password'),
    # 强制需要大小写
    # RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,32}$')
]
