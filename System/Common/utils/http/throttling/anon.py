# -*- encoding: utf-8 -*-
"""
@File Name      :   anon.py    
@Create Time    :   2022/6/7 18:51
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

from rest_framework.throttling import AnonRateThrottle


class AnonSecondRateThrottle(AnonRateThrottle):
    scope = 'anon_second'


class AnonMinuteRateThrottle(AnonRateThrottle):
    scope = 'anon_minute'


class AnonHourRateThrottle(AnonRateThrottle):
    scope = 'anon_hour'


class AnonDayRateThrottle(AnonRateThrottle):
    scope = 'anon_day'
