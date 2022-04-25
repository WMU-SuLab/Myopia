# -*- encoding: utf-8 -*-
"""
@File Name      :   vies.py    
@Create Time    :   2022/4/25 15:48
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


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = 'Screening:manage:index'
    # 因为next是python的关键字，使用next会导致字典获取不到值，所以使用next_url
    redirect_field_name = 'next_url'
