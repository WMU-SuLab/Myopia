# -*- encoding: utf-8 -*-
"""
@File Name      :   feedback.py
@Create Time    :   2022/11/12 20:42
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

from django.core.validators import validate_email as _validate_email
from pydantic import BaseModel, validator

from Common.utils.http.exceptions import ParameterError
from Common.utils.text_handler.validator import validate_phone_number


class UserFeedbackModel(BaseModel):
    name: str
    phone: str
    feedback_content: str
    email: str = None
    wechat_id: str = None

    @validator('email')
    def validate_email(cls, v):
        _validate_email(v)
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ParameterError('手机号格式错误')
        return v

    @validator('feedback_content')
    def validate_feedback_content(cls, v):
        if len(v) > 300:
            raise ParameterError(msg='', chinese_msg='长度不能超过300')
        return v
