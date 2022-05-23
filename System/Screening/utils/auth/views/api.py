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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from Common.utils.auth.permissions import DjangoModelPermissions
from Common.utils.auth.permissions.user import IsMangerUser, IsEmployeeUser, IsInsiderUser


class LoginRequiredView(LoginRequiredMixin, View):
    """
    比较原始，没有办法做更加复杂的用户身份验证，所以用来传页面就可以了，不能用与API
    """
    login_url = 'Screening:manage:index'
    # 因为next是python的关键字，使用next会导致字典获取不到值，所以使用next_url
    redirect_field_name = 'next_url'


class LoginRequiredAPIView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)


class LoginRequiredGenericAPIView(GenericAPIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)


class ManagerLoginRequiredAPIView(LoginRequiredAPIView):
    permission_classes = (IsAuthenticated, IsMangerUser, DjangoModelPermissions)


class ManagerLoginRequiredGenericAPIView(LoginRequiredGenericAPIView):
    permission_classes = (IsAuthenticated, IsMangerUser, DjangoModelPermissions)


class EmployeeLoginRequiredAPIView(LoginRequiredAPIView):
    permission_classes = (IsAuthenticated, IsEmployeeUser, DjangoModelPermissions)


class EmployeeLoginRequiredGenericAPIView(LoginRequiredGenericAPIView):
    permission_classes = (IsAuthenticated, IsEmployeeUser, DjangoModelPermissions)


class InsiderLoginRequiredAPIView(LoginRequiredAPIView):
    permission_classes = (IsAuthenticated, IsInsiderUser, DjangoModelPermissions)


class InsiderLoginRequiredGenericAPIView(LoginRequiredGenericAPIView):
    permission_classes = (IsAuthenticated, IsInsiderUser, DjangoModelPermissions)
