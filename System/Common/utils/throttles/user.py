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


class AdminRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            ident = request.user.pk
            self.scope = 'admin'
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class ManagerRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.is_manager:
            ident = request.user.pk
            self.scope = 'manager'
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class EmployeeRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.is_employee:
            ident = request.user.pk
            self.scope = 'employee'
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
