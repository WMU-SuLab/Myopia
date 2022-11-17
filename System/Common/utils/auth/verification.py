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

from Common.utils.http.exceptions import VerificationCodeError
from Common.utils.text_handler.enum import CodeUsage, code_usage_names
from Common.utils.text_handler.random import generate_verification_code
from Common.viewModels.cache import set_cache, get_cache


def generate_verification_key(identity_field: str, identity: str, usage: str):
    if usage not in code_usage_names:
        return ''
    usage_key = CodeUsage[usage].value
    return f'verification-{identity_field}-{identity}-{usage_key}'


def get_verification_code(identity_field: str, identity: str, usage: str):
    verification_key = generate_verification_key(identity_field, identity, usage)
    return get_cache(verification_key)


def set_verification_code(identity_field: str, identity: str, usage: str):
    verification_code = generate_verification_code(settings.VERIFICATION_CODE_LENGTH)
    verification_key = generate_verification_key(identity_field, identity, usage)
    if get_cache(verification_key):
        raise VerificationCodeError(
            chinese_msg=f'验证码已经发送，仍在有效期内(有效期为{settings.SMS_EXPIRED_TIME / 60}分钟)，请稍后再试')
    set_cache(verification_key, verification_code, settings.SMS_EXPIRED_TIME)
    return verification_code


def verify_verification_code(identity_field: str, identity: str, code: str, usage: str) -> bool:
    if usage not in code_usage_names:
        return False
    verification_key = generate_verification_key(identity_field, identity, usage)
    if not verification_key:
        return False
    verification_code = get_cache(verification_key)
    return verification_code and verification_code == code
