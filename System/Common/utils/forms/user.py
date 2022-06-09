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

from Common.models.user import User
from .validators import phone_validator, password_validators


class PhoneUserForm(forms.Form):
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

    def clean_password(self):
        data = self.cleaned_data
        password: str = data.get('password', None)
        confirm_password: str = data.get('confirm_password', None)
        if not compare_digest(password, confirm_password):
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password


class ResetPasswordForm(forms.Form):
    original_password = forms.CharField(validators=password_validators)
    new_password = forms.CharField(validators=password_validators)
    confirm_password = forms.CharField(validators=password_validators)

    def clean_new_password(self):
        data = self.cleaned_data
        original_password: str = data.get('original_password', None)
        new_password: str = data.get('new_password', None)
        confirm_password: str = data.get('confirm_password', None)
        if compare_digest(original_password, new_password):
            raise forms.ValidationError('新密码不能与原密码相同')
        if not compare_digest(new_password, confirm_password):
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return new_password
