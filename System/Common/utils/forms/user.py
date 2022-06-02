# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/9 19:42
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

from secrets import compare_digest

from django import forms
from django.core.validators import RegexValidator

from Common.models.user import User
from Common.utils.text_handler.validator import validate_phone


class PhoneUserForm(forms.Form):
    password_validators = [
        # 不需要大写
        RegexValidator(r'^(?=.*[a-z])(?=.*\d)[a-zA-Z\d]{6,32}$')
        # 强制需要大小写
        # RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,32}$')
    ]
    phone_validator = [
        validate_phone,
        # RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式不正确')
    ]

    phone = forms.CharField(validators=phone_validator)
    password = forms.CharField(validators=password_validators)
    confirm_password = forms.CharField(validators=password_validators)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', None)
        if not phone:
            raise forms.ValidationError('手机号码不能为空')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('手机号已被注册')
        return phone

    def clean_confirm_password(self):
        data = self.cleaned_data
        password: str = data.get('password', None)
        confirm_password: str = data.get('confirm_password', None)
        if not compare_digest(password, confirm_password):
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password
