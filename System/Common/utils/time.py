# -*- encoding: utf-8 -*-
"""
@File Name      :   time.py    
@Create Time    :   2022/1/11 20:51
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

import functools
import time
from datetime import datetime

from django.conf import settings


# 更精确的运行时间记录
def print_accurate_execute_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'函数 {func.__name__} 耗时 {(end - start) * 1000} ms')
        return res

    return wrapper


def create_tz_time(date_time: datetime):
    return date_time.replace(tzinfo=settings.TZ_INFO).astimezone(settings.TZ_INFO)
