# -*- encoding: utf-8 -*-
"""
@File Name      :   send.py    
@Create Time    :   2022/7/4 19:07
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

from django.conf import settings

from Common.utils.auth.verification import set_verification_code
from Common.utils.http.exceptions import PhoneSendSMSError
from .send import send_sms


def send_verification_sms(phone_number, sign_name, template_code, usage):
    verification_code = set_verification_code('phone_number', phone_number, usage)
    res_data = send_sms(phone_number, sign_name, template_code, json.dumps({
        'code': verification_code,
        'expire_seconds': settings.SMS_EXPIRED_TIME,
        'expire_minutes': settings.SMS_EXPIRED_TIME / 60
    }))
    if res_data.get('Code', '') != 'OK':
        raise PhoneSendSMSError(msg_detail=res_data['Message'], extra=res_data)
    return res_data
