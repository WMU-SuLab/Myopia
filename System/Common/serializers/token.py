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
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from Common.models.user import User
from Common.utils.http.exceptions import UserNotExist, TokenNotExist


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
        data['username'] = refresh.payload['username']
        return data


class ExistMixin:
    def refresh_token_exist(self, token):
        """
        检查token是否存在
        :param token: token
        :return: True/False
        """
        if not OutstandingToken.objects.filter(token=token).exists():
            raise TokenNotExist('Token不存在')
        return True

    def user_exist(self, user_id, username):
        """
        检查用户是否存在
        :param user_id:
        :param username:
        :return: True/False
        """
        if not User.objects.filter(id=user_id, username=username).exists():
            raise UserNotExist('用户不存在')
        return True

    def refresh_is_validate(self, attrs):
        refresh = attrs["refresh"]
        decoded_data = jwt_decode(refresh, settings.SECRET_KEY, algorithms=["HS256"])
        self.user_exist(decoded_data['user_id'], decoded_data['username'])
        return True

    def token_is_validate(self, attrs):
        token = attrs["token"]
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        self.user_exist(decoded_data['user_id'], decoded_data['username'])
        return decoded_data


class TokenRefreshSerializer(ExistMixin, _TokenRefreshSerializer):
    def validate(self, attrs):
        self.refresh_is_validate(attrs)
        data = super().validate(attrs)
        access = data.get('access', None)
        decoded_data = jwt_decode(access, settings.SECRET_KEY, algorithms=["HS256"])
        return {**data, 'exp': decoded_data['exp']}


class TokenVerifySerializer(ExistMixin, _TokenVerifySerializer):
    def validate(self, attrs):
        decoded_data = self.token_is_validate(attrs)
        data = super().validate(attrs)
        return {**data, **decoded_data}


class TokenBlacklistSerializer(ExistMixin, _TokenBlacklistSerializer):
    def validate(self, attrs):
        self.refresh_is_validate(attrs)
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
