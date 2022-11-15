# -*- encoding: utf-8 -*-
"""
@File Name      :   verification.py
@Create Time    :   2022/7/4 18:58
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

from Common.utils.text_handler.enum import CodeUsage, code_usage_names
from Common.utils.text_handler.random import generate_verification_code
from Common.viewModels.cache import set_cache, get_cache


def generate_verification_key(identity: str, usage: str = 'register'):
    if usage not in code_usage_names:
        return ''
    usage_key = CodeUsage[usage].value
    return f'verification-{identity}-{usage_key}'


def get_verification_code(identity: str, usage: str = 'register'):
    verification_key = generate_verification_key(identity, usage)
    return get_cache(verification_key)


def set_verification_code(identity: str, usage: str = 'register'):
    verification_key = generate_verification_key(identity, usage)
    verification_code = generate_verification_code(settings.VERIFICATION_CODE_LENGTH)
    # todo:覆盖还是不覆盖？
    # if get_cache(verification_key):
    #     raise Exception('验证码已经发送，请稍后再试')
    set_cache(verification_key, verification_code, settings.SMS_EXPIRED_TIME)
    return verification_code


def verify_verification_code(identity: str, code: str, usage: str = 'register') -> bool:
    if usage not in code_usage_names:
        return False
    verification_key = generate_verification_key(identity, usage)
    if not verification_key:
        return False
    verification_code = get_cache(verification_key)
    return verification_code and verification_code == code
