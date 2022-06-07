# -*- encoding: utf-8 -*-
"""
@File Name      :   role.py    
@Create Time    :   2022/6/7 18:52
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


class AdminSecondRateThrottle(UserRateThrottle):
    scope = 'admin_second'


class AdminMinuteRateThrottle(UserRateThrottle):
    scope = 'admin_minute'


class AdminHourRateThrottle(UserRateThrottle):
    scope = 'admin_hour'


class AdminDayRateThrottle(UserRateThrottle):
    scope = 'admin_day'


class ManagerSecondRateThrottle(UserRateThrottle):
    scope = 'manager_second'


class ManagerMinuteRateThrottle(UserRateThrottle):
    scope = 'manager_minute'


class ManagerHourRateThrottle(UserRateThrottle):
    scope = 'manager_hour'


class ManagerDayRateThrottle(UserRateThrottle):
    scope = 'manager_day'


class EmployeeSecondRateThrottle(UserRateThrottle):
    scope = 'employee_second'


class EmployeeMinuteRateThrottle(UserRateThrottle):
    scope = 'employee_minute'


class EmployeeHourRateThrottle(UserRateThrottle):
    scope = 'employee_hour'


class EmployeeDayRateThrottle(UserRateThrottle):
    scope = 'employee_day'
