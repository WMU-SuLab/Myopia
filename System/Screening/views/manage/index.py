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

from Screening.utils.auth.views.manage import title, screening_manage_login_required


@screening_manage_login_required
def index(request):
    return render(request, 'Screening/manage/index.html', context={
        'site_title': title,
        'site_header': title,
    })


@screening_manage_login_required
def home(request):
    return render(request, 'Screening/manage/home.html')


@screening_manage_login_required
def statistics(request):
    return render(request, 'Screening/manage/statistics.html')
