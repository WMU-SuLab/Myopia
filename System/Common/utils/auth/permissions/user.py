# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/5/23 10:45
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
from rest_framework.permissions import BasePermission


class IsMangerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_manager)


class IsEmployeeUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_employee)


class IsInsiderUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_manager or request.user.is_employee))
