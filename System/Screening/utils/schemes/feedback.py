# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/22 16:53
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

from typing import Union

from pydantic import BaseModel, validator

from Common.utils.http.exceptions import ParameterError
from Common.utils.schemes.role import StudentRole, TeacherRole


class UserReportFeedbackModel(BaseModel):
    phone: str
    email: str
    name: str = None
    identification_card_number: str
    user_role: Union[StudentRole, TeacherRole]
    feedback_content: str = '无'

    @validator('identification_card_number')
    def validate_identification_card_number(cls, v):
        if v and len(v) != 18 and len(v) != 4:
            raise ParameterError(msg='identification card number length error', chinese_msg='身份证号码长度不正确')
        return v

    @validator('feedback_content')
    def validate_feedback_content(cls, v):
        if len(v) > 300:
            raise ParameterError(msg='', chinese_msg='长度不能超过300')
        return v
