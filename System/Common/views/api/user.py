# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/5/31 17:35
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

from django.core.validators import validate_email
from django.forms import Form
from rest_framework.response import Response

from Common.models.user import User
from Common.utils.alibabacloud.sms.verification import send_verification_sms
from Common.utils.auth.verification import verify_verification_code
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.auth.views.api import IsAuthenticatedAPIView
from Common.utils.auth.views.token import TokenObtainPairView
from Common.utils.email.verification import send_verification_email
from Common.utils.forms.user import PhoneSMSForm, EmailVerificationCodeForm, RegisterByUsernameForm, ResetPasswordForm, \
    RegisterByPhoneSMSForm, \
    ResetPasswordByPhoneSMSForm, RegisterByEmailForm, ResetPasswordByEmailForm
from Common.utils.http.exceptions import ParameterError, ValidationError, VerificationCodeError, ServerError, \
    PhoneSendSMSError, EmailSendError, UserExist
from Common.utils.http.successes import UserRegisterSuccess, UserPasswordUpdateSuccess, PhoneSMSSendSuccess, \
    EmailSendSuccess
from Common.utils.text_handler.validator import validate_phone_number


class RegisterByUsernameAPIView(AllowAnyAPIView):
    def post(self, request, *args, **kwargs):
        form = RegisterByUsernameForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            return Response(UserRegisterSuccess())
        else:
            return Response(ParameterError(msg_detail=str(form.errors)))


class RestPasswordByLoginAPIView(IsAuthenticatedAPIView):
    def post(self, request, *args, **kwargs):
        user: User = request.user
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            if user.check_password(reset_password_form.cleaned_data['original_password']):
                user.set_password(reset_password_form.cleaned_data['new_password'])
                user.save()
                return Response(UserPasswordUpdateSuccess())
            else:
                return Response(ParameterError(msg_detail='原密码错误'))
        else:
            return Response(ParameterError(msg_detail=str(reset_password_form.errors)))


class SendVerificationCodeAPIView(AllowAnyAPIView):
    identity_field = None

    def validate_identity(self, identity):
        raise NotImplementedError()

    def validate(self, request, *args, **kwargs):
        if not self.identity_field:
            raise ServerError(msg_detail='identity_field is not set')
        identity = request.data.get(self.identity_field, None) or \
                   request.POST.get(self.identity_field, None) \
                   or request.GET.get(self.identity_field, None)
        if not identity:
            raise ParameterError(msg_detail=f'{self.identity_field} is required')
        self.validate_identity(identity)
        return identity


class SendPhoneSMSAPIView(SendVerificationCodeAPIView):
    identity_field = 'phone_number'
    sign_name = None
    template_code = None
    usage = None

    def validate_identity(self, identity):
        if not validate_phone_number(identity):
            raise ValidationError(msg_detail=f'{self.identity_field} is invalid')
        if self.usage == 'register' and User.objects.filter(**{self.identity_field: identity}).exists():
            raise UserExist(msg_detail=f'{self.identity_field} is exists', chinese_msg='该用户已经存在')
        return True

    def check_send(self, request):
        res_data = send_verification_sms(self.validate(request), self.sign_name, self.template_code, self.usage)
        if res_data.get('Code') != 'OK':
            return Response(PhoneSendSMSError(msg_detail=res_data.get('Message'), extra=res_data))
        return Response(PhoneSMSSendSuccess())


class SendEmailVerificationCodeAPIView(SendVerificationCodeAPIView):
    identity_field = 'email'
    usage = None

    def validate_identity(self, identity):
        if not validate_email(identity):
            raise ValidationError(msg_detail=f'{self.identity_field} is invalid')
        if self.usage == 'register' and User.objects.filter(**{self.identity_field: identity}).exists():
            raise UserExist(msg_detail=f'{self.identity_field} is exists', chinese_msg='该用户已经存在')
        return True

    def check_send(self, request, *args, **kwargs):
        if send_verification_email(self.validate(request), self.usage):
            return Response(EmailSendSuccess())
        else:
            return Response(EmailSendError(msg_detail='邮件发送失败'))


class VerifyVerificationCodeAPIView(AllowAnyAPIView):
    identity_field = None
    usage = None

    def validate_success(self, form: Form):
        raise NotImplementedError()

    def validate(self, form: Form):
        if form.is_valid():
            if verify_verification_code(
                    form.cleaned_data[self.identity_field],
                    form.cleaned_data['verification_code'],
                    self.usage):
                return self.validate_success(form)
            else:
                return Response(VerificationCodeError(msg_detail='验证码错误或者已过期'))
        else:
            return Response(ParameterError(msg_detail=str(form.errors)))


class RegisterByVerificationCodeAPIView(VerifyVerificationCodeAPIView):
    usage = 'register'

    def validate_success(self, form: Form):
        User.objects.create_user(
            password=form.cleaned_data['password'],
            **{self.identity_field: form.cleaned_data[self.identity_field]})
        return Response(UserRegisterSuccess())


class ResetPasswordByVerificationCodeAPIView(VerifyVerificationCodeAPIView):
    usage = 'reset_password'

    def validate_success(self, form: Form):
        user = User.objects.get(**{self.identity_field: form.cleaned_data[self.identity_field]})
        user.set_password(form.cleaned_data['password'])
        user.save()
        return Response(UserPasswordUpdateSuccess())


class RegisterByPhoneNumberAndVerificationCodeAPIView(RegisterByVerificationCodeAPIView):
    identity_field = 'phone_number'

    def post(self, request, *args, **kwargs):
        form = RegisterByPhoneSMSForm(request.POST)
        return self.validate(form)


class ResetPasswordByPhoneNumberAndVerificationCodeAPIView(ResetPasswordByVerificationCodeAPIView):
    identity_field = 'phone_number'

    def post(self, request, *args, **kwargs):
        form = ResetPasswordByPhoneSMSForm(request.POST)
        return self.validate(form)


class RegisterByEmailAndVerificationCodeAPIView(RegisterByVerificationCodeAPIView):
    identity_field = 'email'

    def post(self, request, *args, **kwargs):
        form = RegisterByEmailForm(request.POST)
        return self.validate(form)


class ResetPasswordByEmailAndVerificationCodeAPIView(ResetPasswordByVerificationCodeAPIView):
    identity_field = 'email'

    def post(self, request, *args, **kwargs):
        form = ResetPasswordByEmailForm(request.POST)
        return self.validate(form)


class RegisterAndLoginAPIView(
    VerifyVerificationCodeAPIView,
    TokenObtainPairView
):
    """
    用于注册并同时登录
    """
    usage = 'register_and_login'

    def validate_success(self, form: Form):
        user = User.objects.filter(**{self.identity_field: form.cleaned_data[self.identity_field]})
        if not user.exists():
            User.objects.create_user(**{self.identity_field: form.cleaned_data[self.identity_field]})

    def post(self, request, *args, **kwargs):
        if request.data.get('phone_number', None):
            self.identity_field = 'phone_number'
            form = PhoneSMSForm(request.data)
        elif request.data.get('email', None):
            self.identity_field = 'email'
            form = EmailVerificationCodeForm(request.data)
        else:
            raise ParameterError(msg_detail='phone_number or email is required')
        self.validate(form)
        return super().post(request, *args, **kwargs)
