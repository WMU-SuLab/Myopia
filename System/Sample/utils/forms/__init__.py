# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/4/9 19:38
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

from django import forms
from django.core.validators import RegexValidator

serial_number = forms.CharField(min_length=9, validators=[
    RegexValidator(
        regex=r'\d{2}[A-Z]{2,3}[a-z0-9]{5,12}',
        message='序列号规则验证错误，不是合法的序列号',
        code='invalid serial_number'
    ),
])
