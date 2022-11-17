# -*- encoding: utf-8 -*-
"""
@File Name      :   verification.py    
@Create Time    :   2022/7/4 18:08
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

from Common.utils.auth.verification import set_verification_code
from . import server_send_mail


def send_verification_email(email, usage='register'):
    verification_code = set_verification_code('email', email, usage)
    message = f'您的验证码是{verification_code}，{settings.SMS_EXPIRED_TIME / 60}分钟内有效，请勿泄露给他人。'
    return server_send_mail('验证码', message, recipient_list=[email])
