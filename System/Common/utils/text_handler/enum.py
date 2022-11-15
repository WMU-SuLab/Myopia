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


def enum_names(enum_items: Enum):
    return [enum_item.name for enum_item in enum_items]


def enum_values(enum_items: Enum):
    return [enum_item.value for enum_item in enum_items]


class CodeUsage(Enum):
    # 和验证相关
    register = 1
    login = 2
    register_and_login = 3
    reset_password = 4
    change_password = 5

    # 和身份相关
    change_username = 10
    change_mobile = 11
    change_email = 12
    change_avatar = 13
    change_qq = 14
    change_wechat = 15


code_usage_names = [code_usage.name for code_usage in CodeUsage]
code_usage_values = [code_usage.value for code_usage in CodeUsage]
