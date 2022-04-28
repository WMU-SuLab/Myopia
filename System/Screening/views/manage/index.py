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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

title = '眼健康筛查管理系统'
login_view_name = 'Screening:manage:login'
login_api_view_name = 'Screening:api:manage:login'
redirect_field_name = 'next_url'
screening_manage_login_required = login_required(login_url=login_view_name, redirect_field_name=redirect_field_name)


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
