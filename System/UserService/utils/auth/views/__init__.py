# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/6/29 18:56
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

login_view_name = 'UserService:sample_login'
login_api_view_name = 'UserService:api:sample_login'


class SampleManagerLoginRequiredMixin(LoginRequiredMixin):
    loin_url = login_view_name
    redirect_field_name = 'next_url'
    permission_denied_message = 'You are not allowed to access this page.'


class SampleManagerLoginRequiredView(SampleManagerLoginRequiredMixin, View):
    pass
