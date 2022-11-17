# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py
@Create Time    :   2022/11/11 21:13
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

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework.response import Response

from Common.models.user import User
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.exceptions import AuthenticationFailed, PermissionDenied, ParameterError
from Sample.utils.auth.views import sample_manager_redirect_field_name
from Sample.utils.auth.views.api import SampleManagerIsAuthenticatedAPIView


class SampleManagerLoginAPIView(AllowAnyAPIView):
    def post(self, request):
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')
        next_url = request.POST.get(sample_manager_redirect_field_name, 'Sample:manage:index')
        if not username or not password:
            return Response(ParameterError())
        user: User = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name='sample_manager'):
                login(request, user)
                return redirect(next_url)
            else:
                return Response(PermissionDenied())
        else:
            return Response(AuthenticationFailed(message='用户名或密码错误'))


class SampleManagerLogoutAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        logout(request)
        return redirect('Sample:manage:login')
