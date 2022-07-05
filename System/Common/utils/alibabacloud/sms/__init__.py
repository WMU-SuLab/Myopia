# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/7/4 19:01
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

from Tea.exceptions import UnretryableException
from alibabacloud_dysmsapi20170525 import models

from Common.utils.alibabacloud import client
from Common.utils.http.exceptions import PhoneSendSMSError, ServerError
from Common.utils.schemes.sms import SendSMSModel


def handle_send_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnretryableException as e:
            print(e.inner_exception)
            raise PhoneSendSMSError(msg_detail=str(e))
        except Exception as e:
            print(e)
            raise ServerError(msg_detail=str(e))

    return wrapper


@handle_send_exception
def send_sms(phone_number, sign_name, template_code, template_param):
    SendSMSModel(phone_number=phone_number, sign_name=sign_name, template_code=template_code,
                 template_param=template_param)
    req = models.SendSmsRequest(
        phone_numbers=phone_number,
        sign_name=sign_name,
        template_code=template_code,
        template_param=template_param
    )
    res = client.send_sms(req)
    return res.body.to_map()
