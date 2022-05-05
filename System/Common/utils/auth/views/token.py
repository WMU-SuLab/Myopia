# -*- encoding: utf-8 -*-
"""
@File Name      :   token.py    
@Create Time    :   2022/4/29 10:48
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

from rest_framework_simplejwt.views import TokenObtainPairView as _TokenObtainPairView, \
    TokenRefreshView as _TokenRefreshView, \
    TokenVerifyView as _TokenVerifyView, TokenBlacklistView as _TokenBlacklistView, \
    TokenObtainSlidingView as _TokenObtainSlidingView, TokenRefreshSlidingView as _TokenRefreshSlidingView

from Common.serializers.token import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer, \
    TokenBlacklistSerializer, TokenObtainSlidingSerializer, TokenRefreshSlidingSerializer


class TokenObtainPairView(_TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer



class TokenRefreshView(_TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class TokenVerifyView(_TokenVerifyView):
    serializer_class = TokenVerifySerializer


class TokenBlacklistView(_TokenBlacklistView):
    serializer_class = TokenBlacklistSerializer


class TokenObtainSlidingView(_TokenObtainSlidingView):
    serializer_class = TokenObtainSlidingSerializer


class TokenRefreshSlidingView(_TokenRefreshSlidingView):
    serializer_class = TokenRefreshSlidingSerializer
