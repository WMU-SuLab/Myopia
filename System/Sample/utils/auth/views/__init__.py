# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
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

sample_manage_title = '采样管理后台'
sample_manager_login_view_name = 'Sample:manage:login'
sample_manager_login_api_view_name = 'Sample:api:manage:login'
sample_manager_redirect_field_name = 'next_url'


class SampleManagerLoginRequiredMixin(LoginRequiredMixin):
    login_url = sample_manager_login_view_name
    redirect_field_name = sample_manager_redirect_field_name
    permission_denied_message = 'You are not allowed to access this page.'


class SampleManagerLoginRequiredView(SampleManagerLoginRequiredMixin, View):
    pass
