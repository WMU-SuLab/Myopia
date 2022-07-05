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

from Common.utils.auth.verification import set_verification_code
from Common.utils.http.exceptions import PhoneSendSMSError
from . import send_sms


def send_verification_sms(phone_number, sign_name, template_code, usage='register'):
    verification_code = set_verification_code(phone_number, usage)
    res_data = send_sms(phone_number, sign_name, template_code, json.dumps({'code': verification_code}))
    if res_data['Code'] != 'OK':
        raise PhoneSendSMSError(msg_detail=res_data['Message'], extra=res_data)
    return res_data
