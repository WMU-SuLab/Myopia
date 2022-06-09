# -*- encoding: utf-8 -*-
"""
@File Name      :   token.py    
@Create Time    :   2022/5/3 19:59
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

from django.conf import settings
from jwt import decode as jwt_decode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as _TokenObtainPairSerializer, \
    TokenRefreshSerializer as _TokenRefreshSerializer, TokenVerifySerializer as _TokenVerifySerializer, \
    TokenBlacklistSerializer as _TokenBlacklistSerializer, \
    TokenObtainSlidingSerializer as _TokenObtainSlidingSerializer, \
    TokenRefreshSlidingSerializer as _TokenRefreshSlidingSerializer


class TokenObtainPairSerializer(_TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        此方法往token的有效负载 payload 里面添加数据
        例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
        这部分放在token里面是可以被解析的，所以不要放比较私密的信息
        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        token['username'] = user.username
        return token

    def validate(self, attrs):
        """
        此方法为响应数据结构处理
        原有的响应数据结构无法满足需求，在这里重写结构
        :param attrs: 請求參數
        :return: 响应数据
        """
        data = super().validate(attrs)
        # 获取Token对象
        refresh = self.get_token(self.user)
        # data['refresh_token'] = str(refresh)
        # 令牌到期时间
        data['refresh_expire_at'] = refresh.payload['exp']
        data['access_expire_at'] = refresh.access_token.payload['exp']
        data['username'] = self.user.username
        return data


class TokenRefreshSerializer(_TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data


class TokenVerifySerializer(_TokenVerifySerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_data = jwt_decode(attrs['token'], settings.SECRET_KEY, algorithms=["HS256"])
        return {**data, **decoded_data}


class TokenBlacklistSerializer(_TokenBlacklistSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data


class TokenObtainSlidingSerializer(_TokenObtainSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data


class TokenRefreshSlidingSerializer(_TokenRefreshSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        return data
