# -*- encoding: utf-8 -*-
"""
@File Name      :   api.py    
@Create Time    :   2022/5/17 17:11
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

from rest_framework.permissions import IsAuthenticated

from Common.utils.auth.permissions import DjangoModelPermissions
from Common.utils.auth.permissions.user import IsMangerUser, IsEmployeeUser, IsInsiderUser
from Common.utils.auth.views.api import IsAuthenticatedAPIView, IsAuthenticatedGenericAPIView


class ManagerIsAuthenticatedAPIView(IsAuthenticatedAPIView):
    permission_classes = (IsAuthenticated, IsMangerUser)


class ManagerIsAuthenticatedGenericAPIView(IsAuthenticatedGenericAPIView):
    permission_classes = (IsAuthenticated, IsMangerUser, DjangoModelPermissions)


class EmployeeIsAuthenticatedAPIView(IsAuthenticatedAPIView):
    permission_classes = (IsAuthenticated, IsEmployeeUser)


class EmployeeIsAuthenticatedGenericAPIView(IsAuthenticatedGenericAPIView):
    permission_classes = (IsAuthenticated, IsEmployeeUser, DjangoModelPermissions)


class InsiderIsAuthenticatedAPIView(IsAuthenticatedAPIView):
    permission_classes = (IsAuthenticated, IsInsiderUser)


class InsiderIsAuthenticatedGenericAPIView(IsAuthenticatedGenericAPIView):
    permission_classes = (IsAuthenticated, IsInsiderUser, DjangoModelPermissions)
