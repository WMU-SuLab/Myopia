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

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email

from Common.models.role import WeChatAPPRole, WeChatPlatformRole
from Common.utils.auth.verification import verify_verification_code
from Common.utils.http.exceptions import AuthenticationFailed
from Common.utils.http.exceptions import ValidationError, ParameterError
from Common.utils.http.wechat import WeChatApi
from Common.utils.text_handler.validator import validate_phone_number

UserModel = get_user_model()


class UserBackend(ModelBackend):
    def authenticate(self, request, username: str = None, password: str = None, **kwargs):
        email = kwargs.get('email', None)
        phone_number = kwargs.get('phone_number', None)
        app_name = kwargs.get('app_name', None)
        platform_name = kwargs.get('platform_name', None)
        verification_code = kwargs.get('verification_code', None)
        # user = UserModel._default_manager.get_by_natural_key(username)
        if username or email or phone_number:
            user = None
            if username:
                # user = UserModel.objects.get(
                #     Q(username__iexact=username) | Q(email__iexact=username) | Q(phone_number__iexact=username) |
                #     Q(wechat_roles__open_id__iexact=username) | Q(wechat_roles__union_id__iexact=username)
                # )
                user = UserModel.objects.get(username=username)
            elif username := kwargs.get(UserModel.USERNAME_FIELD, ''):
                user = UserModel.objects.get(**{UserModel.USERNAME_FIELD: username})
            elif email:
                if not validate_email(email):
                    raise ValidationError('Invalid email address.')
                user = UserModel.objects.get(email=email)
            elif phone_number:
                if not validate_phone_number(phone_number):
                    raise ValidationError('Invalid phone number.')
                user = UserModel.objects.get(phone_number=phone_number)
            # 验证用户是否存在
            if not user:
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
                email_login = verify_verification_code('email', email, verification_code, 'login') if email else False
                email_register_and_login = verify_verification_code(
                    'email', email, verification_code, 'register_and_login') if email else False
                phone_number_login = verify_verification_code('phone_number', phone_number, verification_code, 'login') \
                    if phone_number else False
                phone_number_register_and_login = verify_verification_code(
                    'phone_number', phone_number, verification_code, 'register_and_login') if phone_number else False
                if email_login or email_register_and_login or phone_number_login or phone_number_register_and_login:
                    return user if self.user_can_authenticate(user) else None
                else:
                    raise ValidationError(msg='Verification_code is incorrect.', chinese_msg='验证码错误')
            else:
                raise ParameterError('password or verification_code is required')
            # return super().authenticate(request, username, password, **kwargs)
        elif app_name or platform_name:
            if app_name and verification_code:
                app = settings.WECHAT_MINAS.get(app_name, {})
                if not app:
                    raise ParameterError('Invalid app name.')
                app_id = app['app_id']
                secret_key = app['secret_key']
                wechat_mina_api = WeChatApi(app_id, secret_key)
                res_json = wechat_mina_api.get_openid_and_session_key(verification_code)
                # 成功了是没有errcode和errmsg的
                if errcode := res_json.get('errcode', 0) != 0:
                    raise AuthenticationFailed(msg=errcode, msg_detail=res_json.get('errmsg', ''))
                open_id = res_json['openid']
                session_key = res_json['session_key']
                user = UserModel.objects.get(wechat_app_roles__app_name=app_name, wechat_app_roles__open_id=open_id)
                if not user:
                    user = UserModel.objects.create_user()
                wechat_app_role, wechat_app_role_exist = WeChatAPPRole.objects.get_or_create(
                    user=user, app_name=app_name, open_id=open_id)
                wechat_app_role.session_key = session_key
                if union_id := res_json.get('unionid', ''):
                    wechat_platform_role, wechat_platform_role_exist = WeChatPlatformRole.objects.get_or_create(
                        user=user, union_id=union_id, platform_name=platform_name)
                    wechat_app_role.session_key = session_key
                    wechat_platform_role.save()
                    wechat_app_role.platform_role = wechat_platform_role
                wechat_app_role.save()
                return user if self.user_can_authenticate(user) else None
            if platform_name and verification_code:
                pass
        else:
            raise ParameterError('username or email or phone_number app_name or platform_name  is required')
