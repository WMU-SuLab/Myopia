# -*- encoding: utf-8 -*-
"""
@File Name      :   authentication.py    
@Create Time    :   2022/4/7 20:45
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

from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication as _JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from Common.models.user import User


class JWTAuthentication(_JWTAuthentication):
    """
    修改JWT认证类，返回自定义User表对象
    只是用于验证token的合法性，而不是验证用户的权限(permission)，那是确定token是合法且能够使用之后再进行验证的事情
    """

    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        return user
