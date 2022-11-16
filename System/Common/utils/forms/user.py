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
from django.conf import settings

from Common.models.user import User
from .validators import phone_number_validators, password_validators


class PasswordForm(forms.Form):
    password = forms.CharField(validators=password_validators)
    confirm_password = forms.CharField(validators=password_validators)

    def clean_confirm_password(self):
        data = self.cleaned_data
        password: str = data.get('password', None)
        confirm_password: str = data.get('confirm_password', None)
        if not compare_digest(password, confirm_password):
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return password


class PhoneSMSForm(forms.Form):
    phone_number = forms.CharField(validators=phone_number_validators)
    verification_code = forms.CharField(
        min_length=settings.VERIFICATION_CODE_LENGTH,
        max_length=settings.VERIFICATION_CODE_LENGTH)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number:
            raise forms.ValidationError('手机号码不能为空')
        return phone_number


class EmailVerificationCodeForm(forms.Form):
    email = forms.EmailField()
    verification_code = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if not email:
            raise forms.ValidationError('邮箱不能为空')
        return email


class RegisterByUsernameForm(PasswordForm):
    username = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if not username:
            raise forms.ValidationError('用户名不能为空')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已被注册')
        return username


class ResetPasswordForm(forms.Form):
    original_password = forms.CharField(validators=password_validators)
    new_password = forms.CharField(validators=password_validators)
    confirm_password = forms.CharField(validators=password_validators)

    def clean_new_password(self):
        data = self.cleaned_data
        original_password: str = data['original_password']
        new_password: str = data['new_password']
        if compare_digest(original_password, new_password):
            raise forms.ValidationError('新密码不能与原密码相同')
        return new_password

    def clean_confirm_password(self):
        data = self.cleaned_data
        new_password: str = data['new_password']
        confirm_password: str = data['confirm_password']
        if not compare_digest(new_password, confirm_password):
            raise forms.ValidationError('两次输入的密码不一致，请修改!')
        return confirm_password


class RegisterByPhoneSMSForm(PhoneSMSForm, PasswordForm):
    def clean_phone_number(self):
        phone_number = super().clean_phone_number()
        # if User.objects.filter(Q(phone_number=phone_number) | Q(username=phone_number)).exists():
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('手机号已被注册')
        return phone_number


class ResetPasswordByPhoneSMSForm(PhoneSMSForm, PasswordForm):
    pass


class RegisterByEmailForm(EmailVerificationCodeForm, PasswordForm):
    def clean_email(self):
        email = super().clean_email()
        # if User.objects.filter(Q(email=email) | Q(username=email)).exists():
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email


class ResetPasswordByEmailForm(EmailVerificationCodeForm, PasswordForm):
    pass
