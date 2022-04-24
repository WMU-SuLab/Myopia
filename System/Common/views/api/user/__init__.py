# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/4/24 15:45
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

from Common.utils.auth.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .session import session_login, session_logout

urlpatterns = [
    path('session-login', session_login, name='session_login'),
    path('session-logout', session_logout, name='session_logout'),
    path('token-login', TokenObtainPairView.as_view(), name='token_login'),
    path('token-logout', TokenBlacklistView.as_view(), name='token_logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
