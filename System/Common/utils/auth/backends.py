# -*- encoding: utf-8 -*-
"""
@File Name      :   backends.py    
@Create Time    :   2022/4/7 17:15
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

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend,ModelBackend
from django.db.models import Q
from rest_framework_simplejwt.serializers import ValidationError

UserModel = get_user_model()

# todo：完善用户认证后端
class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # user = UserModel._default_manager.get_by_natural_key(username)
            # You can customise what the given username is checked against, here I compare to both
            # username and email fields of the User model
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username) | Q(phone=username)

            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return super().authenticate(request, username, password, **kwargs)


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print(request.data) 参考请求的其他数据
        # print(request.data['demo']) 比如说key是demo的数据用来做你要的数据校验
        try:
            # 小编这里添加了一个手机验证，如果需要其他验证再加就ok了
            try:
                user = UserModel.objects.get(Q(username=username) | Q(phone=username))
            except Exception:
                raise ValidationError({'': '账号没有注册'})

            if user.check_password(password):
                return user
            else:
                # 如果不想密码登录也可以验证码在这里写
                # 这里做验证码的操作
                raise ValidationError({'': '密码错误'})

        except Exception as e:
            raise e


class OpenIdAuth(BaseBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, openid=None, **kwargs):
        if openid is None:
            return
        try:
            user = UserModel.objects.get(openid=openid)
        except UserModel.DoesNotExist:
            return None
        else:
            # if user is not None:
            #     return user
            # return None
            return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

