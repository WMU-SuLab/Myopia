# -*- encoding: utf-8 -*-
"""
@File Name      :   index.py    
@Create Time    :   2022/7/9 21:31
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


class Index(AllowAnyAPIView):
    def get(self, request):
        return render(request, 'index.html')
