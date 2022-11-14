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
from django.core.validators import validate_email
from django.db.models import Q

from Common.utils.auth.verification import verify_verification_code
from Common.utils.http.exceptions import ValidationError, ParameterError
from Common.utils.text_handler.validator import validate_phone_number

UserModel = get_user_model()


class UserBackend(ModelBackend):
    def authenticate(self, request, username: str = None, password: str = None, **kwargs):
        email = kwargs.get('email', None)
        phone_number = kwargs.get('phone_number', None)
        open_id = kwargs.get('open_id', None)
        union_id = kwargs.get('union_id', None)
        verification_code = kwargs.get('verification_code', None)
        # user = UserModel._default_manager.get_by_natural_key(username)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, '')
        if username:
            user = UserModel.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username) | Q(phone_number__iexact=username) |
                Q(wechat_roles__open_id__iexact=username) | Q(wechat_roles__union_id__iexact=username)
            )
        elif email:
            user = UserModel.objects.filter(email=email)
        elif phone_number:
            user = UserModel.objects.filter(phone_number=phone_number)
        elif open_id:
            user = UserModel.objects.filter(wechat_role__open_id=open_id)
        elif union_id:
            user = UserModel.objects.filter(wechat_role__union_id=union_id)
        else:
            raise ParameterError('username or email or phone_number or open_id or union_id is required')
        # 验证用户是否存在
        if user.exists():
            user = user.first()
        else:
            raise ValidationError(msg='User dose not exist.', chinese_msg='用户不存在')
        # 验证用户密码或者验证码
        if password:
            if user.check_password(password):
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                # 使用密码验证
                return user if self.user_can_authenticate(user) else None
            else:
                # UserModel().set_password(password)
                raise ValidationError(msg='Password is incorrect.', chinese_msg='密码错误')
        elif verification_code:
            if (email and validate_email(email) and verify_verification_code(email, verification_code, 'login')) or \
                    (phone_number and validate_phone_number(phone_number)
                     and verify_verification_code(phone_number, verification_code, 'login')):
                # todo:考虑登录之后是否需要删除验证码，不允许再使用
                return user if self.user_can_authenticate(user) else None
            else:
                raise ValidationError(msg='Verification_code is incorrect.', chinese_msg='验证码错误')
        # todo:完善微信的登录验证
        else:
            raise ParameterError('password or verification_code is required')
        # return super().authenticate(request, username, password, **kwargs)
