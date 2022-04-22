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

from UserService.utils.schemes.role import StudentRole, TeacherRole


class UserFeedback(BaseModel):
    name: str
    identification_card_number: str
    user_role: Union[StudentRole, TeacherRole]
    phone: str
    email: str
    feedback_content: str = '无'

    @validator('feedback_content')
    def validate_feedback_content(cls, v):
        if len(v) > 300:
            raise ValueError('长度不能超过300')
        return v
