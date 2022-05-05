# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/14 9:52
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

from django.shortcuts import render, reverse

from .index import title, login_api_view_name, screening_manage_login_required


def login(request):
    return render(request, 'Screening/manage/login.html', context={
        'site_title': title,
        'site_header': title,
        'app_path': reverse(login_api_view_name)
    })


@screening_manage_login_required
def user(request):
    return render(request, 'Screening/manage/user.html')
