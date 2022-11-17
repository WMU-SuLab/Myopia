# -*- encoding: utf-8 -*-
"""
@File Name      :   choices.py
@Create Time    :   2022/11/13 18:16
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

from typing import Any

from django.db import models


def reverse_choices(choices: tuple[tuple] or models.Choices):
    if isinstance(choices, tuple):
        return tuple(reversed(choice) for choice in choices)
    elif isinstance(choices, models.Choices):
        return models.Choices(tuple(reversed(choice) for choice in choices.choices))
    else:
        raise TypeError('choices must be tuple or models.Choices')


def choices_to_dict(choices: tuple[tuple] or models.Choices) -> dict:
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


def get_choices_key(choices: tuple[tuple] or models.Choices, choice_value: str, strict: bool = False) -> str or int:
    """
    :param choices:
    :param choice_value:
    :param strict:模糊匹配或者严格匹配
    :return:
    """
    choices_dict = reverse_choices_to_dict(choices)
    if strict:
        return choices_dict.get(choice_value, None)
    for v, k in choices_dict.items():
        if choice_value in v:
            return k
    return None


def choices_to_list(choices: tuple[tuple] or models.Choices, mode: str = 'val') -> list:
    return list(choices_to_dict(choices).values()) if mode == 'val' else list(choices_to_dict(choices).keys())


def list_to_choices(choices: list) -> tuple[tuple[Any, Any], ...]:
    return tuple((v, v) for v in choices)


def same_choices(choices: tuple[tuple] or models.Choices, mode: str = 'val') -> tuple[tuple[Any, Any], ...]:
    return list_to_choices(choices_to_list(choices, mode))
