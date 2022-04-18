# -*- encoding: utf-8 -*-
"""
@File Name      :   index.py    
@Create Time    :   2022/4/17 18:59
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


def index(request):
    return render(request, 'Screening/manage/index.html')