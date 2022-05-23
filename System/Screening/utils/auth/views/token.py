# -*- encoding: utf-8 -*-
"""
@File Name      :   token.py    
@Create Time    :   2022/5/17 16:32
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

from Common.utils.auth.permissions.user import IsEmployeeUser
from Common.utils.auth.views.token import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView


class EmployeeTokenPermission:
    permission_classes = TokenObtainPairView.permission_classes + (
        IsEmployeeUser,) if TokenObtainPairView.permission_classes else (IsEmployeeUser,)


class EmployeeTokenObtainPairView(TokenObtainPairView, EmployeeTokenPermission):
    pass


class EmployeeTokenRefreshView(TokenRefreshView, EmployeeTokenPermission):
    pass


class EmployeeTokenVerifyView(TokenVerifyView, EmployeeTokenPermission):
    pass


class EmployeeTokenBlacklistView(TokenBlacklistView, EmployeeTokenPermission):
    pass
