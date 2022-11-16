# -*- encoding: utf-8 -*-
"""
@File Name      :   validator.py    
@Create Time    :   2022/4/25 11:14
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

import re


def validate_length(pwd, min_=8, max_=16):
    if min_ <= len(pwd) <= max_:
        return True, None
    else:
        return False, "密码长度应在8到16位"


def validate_number(pwd):
    match = re.search(r"\d+", pwd)
    if match:
        return True, None
    else:
        return False, "密码应该包含数字"


def validate_upper(pwd):
    res = re.search("[A-Z]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该包含大写字母"


def validate_lower(pwd):
    res = re.search("[a-z]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该包含小写字母"


def validate_start(pwd):
    res = re.search(r"^[a-zA-Z\d]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该以字母或数字开头"


def check_special(pwd):
    res = re.search(r"[~!@#$%^&*()\-_=+]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该至少包含一个特殊字符"


def validate_password(pwd):
    # 想校验什么就把方法名添加到这个list里
    for temp in [validate_length, validate_number, validate_upper, validate_lower, validate_start, check_special]:
        is_ok, error = temp(pwd)
        if not is_ok:
            return False, error
    return True, None


def validate_tel_number(tel_number: str) -> bool:
    """
    验证座机号码
    :param tel_number:
    :return:
    """
    match = re.match(r"^0\d{2,3}-\d{7,8}$", tel_number)
    if match:
        return True
    else:
        return False


def validate_phone_number(phone_number: str) -> bool:
    """
    验证手机号码
    :param phone_number:
    :return:
    """
    if 11 <= len(phone_number) <= 20:
        if len(phone_number) == 11 and phone_number.isdigit():
            return True
        else:
            region_match = re.match(r'\+\d{1,3} ', phone_number)
            if region_match:
                region = region_match.group(0)
                phone_number_number = phone_number.replace(region, '')
                if region and phone_number_number.isdigit():
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False
