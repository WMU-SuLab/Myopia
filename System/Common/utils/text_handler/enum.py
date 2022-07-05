# -*- encoding: utf-8 -*-
"""
@File Name      :   enum.py    
@Create Time    :   2022/7/4 17:59
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

from enum import Enum


class CodeUsage(Enum):
    register = 1
    login = 2
    reset_password = 3
    change_password = 4
    change_mobile = 5
    change_email = 6
