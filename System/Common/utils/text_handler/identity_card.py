# -*- encoding: utf-8 -*-
"""
@File Name      :   identity_card.py    
@Create Time    :   2022/4/8 17:35
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

from django.conf import settings
from django.utils import timezone


def is_identity_card(identity_card: str):
    if len(identity_card) != 18:
        return False
    if not identity_card[0:17].isdigit():
        return False
    return True


def get_birthday(identity_card: str):
    if is_identity_card(identity_card):
        return identity_card[6:14]
    else:
        return None


def get_sex(identity_card: str):
    if is_identity_card(identity_card):
        if int(identity_card[16]) == 0:
            return 'female'
        else:
            return 'male'
    else:
        return None


def get_age(identity_card: str):
    if is_identity_card(identity_card):
        return (timezone.now() - timezone.datetime.strptime(identity_card[6:14], '%Y%m%d').astimezone(
            settings.TZ_INFO)).days // 365
    else:
        return None
