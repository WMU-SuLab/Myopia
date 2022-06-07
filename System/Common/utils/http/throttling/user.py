# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/1 20:54
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

from rest_framework.throttling import UserRateThrottle


class UserSecondRateThrottle(UserRateThrottle):
    scope = 'user_second'


class UserMinuteRateThrottle(UserRateThrottle):
    scope = 'user_minute'


class UserHourRateThrottle(UserRateThrottle):
    scope = 'user_hour'


class UserDayRateThrottle(UserRateThrottle):
    scope = 'user_day'
