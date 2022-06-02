# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/24 9:18
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

from django.urls import path

from Common.utils.auth.views.token import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .file import DownloadFileAPIView,DownloadImageAPIView
from .regions import get_countries, get_provinces, get_cities, get_areas, get_streets
from .test import test
from .user import register, reset_password
from .info import GenderAPIView,EducationAPIView,NationalityAPIView

urlpatterns = [
    path('test', test, name='test'),
    # 用户
    path('user/register', register, name='user_register'),
    path('user/reset_password', reset_password, name='user_rest_password'),
    path('user/login', TokenObtainPairView.as_view(), name='user_login'),
    path('user/logout', TokenBlacklistView.as_view(), name='user_logout'),
    path('user/token/refresh', TokenRefreshView.as_view(), name='user_token_refresh'),
    path('user/token/verify', TokenVerifyView.as_view(), name='user_token_verify'),
    # 下载文件
    path('download_file/<str:encrypted_file_text>', DownloadFileAPIView.as_view(), name='download_file'),
    path('download_image/<str:encrypted_file_text>', DownloadImageAPIView.as_view(), name='download_image'),
    # 地区
    path('get_countries', get_countries, name='get_countries'),
    path('get_provinces/<int:country_id>', get_provinces, name='get_provinces'),
    path('get_cities/<int:province_id>', get_cities, name='get_cities'),
    path('get_areas/<int:city_id>', get_areas, name='get_areas'),
    path('get_streets/<int:area_id>', get_streets, name='get_streets'),
    # 个人信息
    path('info/gender',GenderAPIView.as_view(),name='info_gender'),
    path('info/education', EducationAPIView.as_view(), name='info_education'),
    path('info/nationality', NationalityAPIView.as_view(), name='info_nationality'),
]
