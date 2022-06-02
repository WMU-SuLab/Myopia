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


def choices_to_dict(choices: tuple[tuple] or models.Choices):
    if isinstance(choices, tuple):
        return {k: v for k, v in choices}
    elif isinstance(choices, models.Choices):
        return {k: v for k, v in choices.choices}
    else:
        raise TypeError('choices must be tuple or models.Choices')


def reverse_choices_to_dict(choices: tuple[tuple] or models.Choices) -> dict:
    """
    将choices的逆序转换为字典
    """
    if isinstance(choices, tuple):
        return {v: k for k, v in choices}
    elif isinstance(choices, models.Choices):
        return {v: k for k, v in choices.choices}
    else:
        raise TypeError('choices must be tuple or models.Choices')


def get_choices_key(choices, choice_value):
    choices_dict = choices_to_dict(choices)
    for k, v in choices_dict.items():
        if choice_value in v:
            return k
    return None


def get_choices_key_strict(choices, choice_value):
    return reverse_choices_to_dict(choices).get(choice_value, None)
