# -*- encoding: utf-8 -*-
"""
@File Name      :   role.py    
@Create Time    :   2022/4/21 16:47
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


class StudentRole(BaseModel):
    role_name: str
    student_number: str

    @validator('role_name')
    def validate_name(cls, v):
        if v != 'student':
            raise ValueError('role name not match other fields')
        return v

    def __str__(self):
        return f'{self.role_name}-{self.student_number}'


class TeacherRole(BaseModel):
    role_name: str
    teacher_number: str

    @validator('role_name')
    def validate_name(cls, v):
        if v != 'teacher':
            raise ValueError('role name not match other fields')
        return v

    def __str__(self):
        return f'{self.role_name}-{self.teacher_number}'
