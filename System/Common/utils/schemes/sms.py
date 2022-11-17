# -*- encoding: utf-8 -*-
"""
@File Name      :   sms.py    
@Create Time    :   2022/7/4 22:48
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

from pydantic import BaseModel, validator

from Common.utils.http.exceptions import ParameterError
from Common.utils.text_handler.validator import validate_phone_number as _validate_phone_number


class SendSMSModel(BaseModel):
    phone_number: str
    sign_name: str
    template_code: str
    template_param: str

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not _validate_phone_number(v):
            raise ParameterError(msg='phone number not valid', chinese_msg='手机号码不合法')
        return v
