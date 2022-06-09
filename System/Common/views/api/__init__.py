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
from .file import DownloadFileAPIView, DownloadImageAPIView
from .info import GenderAPIView, EducationAPIView, NationalityAPIView
from .regions import CountryListAPIView, ProvinceListAPIView, CityListAPIView, AreaListAPIView, StreetListAPIView
from .test import test
from .user import register, RestPasswordAPIView

urlpatterns = [
    path('test', test, name='test'),
    # 用户
    path('user/register', register, name='user_register'),
    path('user/reset_password', RestPasswordAPIView.as_view(), name='user_rest_password'),
    path('user/login', TokenObtainPairView.as_view(), name='user_login'),
    path('user/logout', TokenBlacklistView.as_view(), name='user_logout'),
    path('user/token/refresh', TokenRefreshView.as_view(), name='user_token_refresh'),
    path('user/token/verify', TokenVerifyView.as_view(), name='user_token_verify'),
    # 下载文件
    path('download_file/<str:encrypted_file_text>', DownloadFileAPIView.as_view(), name='download_file'),
    path('download_image/<str:encrypted_file_text>', DownloadImageAPIView.as_view(), name='download_image'),
    # 地区
    path('countries', CountryListAPIView.as_view(), name='get_countries'),
    path('provinces/<int:country_id>', ProvinceListAPIView.as_view(), name='get_provinces'),
    path('cities/<int:province_id>', CityListAPIView.as_view(), name='get_cities'),
    path('areas/<int:city_id>', AreaListAPIView.as_view(), name='get_areas'),
    path('streets/<int:area_id>', StreetListAPIView.as_view(), name='get_streets'),
    # 个人信息
    path('info/gender', GenderAPIView.as_view(), name='info_gender'),
    path('info/education', EducationAPIView.as_view(), name='info_education'),
    path('info/nationality', NationalityAPIView.as_view(), name='info_nationality'),
]
