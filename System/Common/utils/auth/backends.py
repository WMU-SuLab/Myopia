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
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from Common.utils.auth.validator import validate_verification_code
from Common.utils.http.exceptions import ValidationError, ParameterError

UserModel = get_user_model()


# todo:完善微信的登录
class UserBackend(ModelBackend):
    def authenticate(self, request, username: str = None, password: str = None, **kwargs):
        email = kwargs.get('email', None)
        phone = kwargs.get('phone', None)
        open_id = kwargs.get('open_id', None)
        union_id = kwargs.get('union_id', None)
        verification_code = kwargs.get('verification_code', None)
        # user = UserModel._default_manager.get_by_natural_key(username)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, '')
        if username:
            user = UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username) | Q(phone__iexact=username) |
                Q(wechat_role__open_id__iexact=username) | Q(wechat_role__union_id__iexact=username)
            )
        elif email:
            user = UserModel.objects.filter(email=email)
        elif phone:
            user = UserModel.objects.filter(phone=phone)
        elif open_id:
            user = UserModel.objects.filter(wechat_role__open_id=open_id)
        elif union_id:
            user = UserModel.objects.filter(wechat_role__union_id=union_id)
        else:
            raise ParameterError('username or email or phone or open_id or union_id is required')

        if user.exist():
            user = user.first()
        else:
            raise ValidationError(msg='User dose not exist.', chinese_msg='用户不存在')

        if password:
            if user.check_password(password) and self.user_can_authenticate(user):
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                # 使用密码验证
                return user if self.user_can_authenticate(user) else None
            else:
                # UserModel().set_password(password)
                raise ValidationError(msg='Password is incorrect.', chinese_msg='密码错误')
        elif verification_code:
            if validate_verification_code(
                    verification_code=verification_code,
                    username=username,
                    email=email,
                    phone=phone):
                # 使用验证码验证
                return user if self.user_can_authenticate(user) else None
            else:
                # UserModel().set_password(password)
                raise ValidationError(msg='Verification_code is incorrect.', chinese_msg='验证码错误')
        else:
            raise ParameterError('password or verification_code is required')
        # return super().authenticate(request, username, password, **kwargs)
