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


def validate_phone(phone: str) -> bool:
    """
    验证手机号码
    :param phone:
    :return:
    """
    if 11 <= len(phone) <= 20:
        if len(phone) == 11 and phone.isdigit():
            return True
        else:
            region_match = re.match(r'\+\d{1,3} ', phone)
            if region_match:
                region = region_match.group(0)
                phone_number = phone.replace(region, '')
                if region and phone_number.isdigit():
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False
