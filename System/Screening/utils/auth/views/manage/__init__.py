# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/7/1 15:53
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

title = '眼健康筛查管理系统'
login_view_name = 'Screening:manage:login'
login_api_view_name = 'Screening:api:manage:login'
redirect_field_name = 'next_url'
screening_manage_login_required = login_required(redirect_field_name=redirect_field_name, login_url=login_view_name)
