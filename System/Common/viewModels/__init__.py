# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/11 20:18
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

from django.db import models


def reverse_choices(choices: tuple[tuple] or models.Choices) -> dict:
    """
    将choices的逆序转换为字典
    """
    if isinstance(choices, tuple):
        return {v: k for k, v in choices}
    elif isinstance(choices, models.Choices):
        return {v: k for k, v in choices.choices}
    else:
        raise TypeError('choices must be tuple or models.Choices')
