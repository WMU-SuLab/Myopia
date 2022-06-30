# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2022/6/29 15:28
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

from django.shortcuts import render

from Common.utils.auth.views.api import AllowAnyAPIView
from UserService.utils.auth.views import SampleManagerLoginRequiredView


class SampleManagerLoginView(AllowAnyAPIView):
    def get(self, request):
        return render(request, 'UserService/sample/login.html')


class SampleManagerIndexView(SampleManagerLoginRequiredView):
    def get(self, request):
        return render(request, 'UserService/sample/index.html')
