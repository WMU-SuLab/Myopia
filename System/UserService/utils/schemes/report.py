# -*- encoding: utf-8 -*-
"""
@File Name      :   report.py    
@Create Time    :   2022/4/23 12:04
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

from datetime import datetime
from typing import Union

from pydantic import BaseModel, validator

from UserService.utils.schemes.role import StudentRole, TeacherRole


class UserReportSearchForm(BaseModel):
    identification_card_number: str
    user_role: Union[StudentRole, TeacherRole]
    name: str = None
    project_name: str = None
    finished_time: datetime = None

    @validator('name')
    def validate_name(cls, v):
        if len(v) > 20:
            raise ValueError('姓名长度不能超过20个字符')
        return v

    @validator('identification_card_number')
    def validate_identification_card_number(cls, v):
        if len(v) != 4:
            raise ValueError('只需要输入身份证号后4位')
        return v
