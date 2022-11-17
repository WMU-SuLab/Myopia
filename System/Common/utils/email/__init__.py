# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/4/15 11:38
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

import functools
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail as _send_mail, send_mass_mail as _send_mass_mail, \
    mail_admins as _mail_admins, mail_managers as _mail_managers

from Common.utils.http.exceptions import EmailBadHeaderError, EmailSendError
from Common.utils.http.successes import EmailSendSuccess


def handle_send_mail(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except BadHeaderError as e:
            return EmailBadHeaderError()
        except SMTPException as e:
            return EmailSendError(msg=str(e))
        return EmailSendSuccess(data=res)

    return wrapper


@handle_send_mail
def send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
        auth_user=None,
        auth_password=None,
        connection=None,
        html_message=None, ):
    return _send_mail(
        subject, message, from_email, recipient_list, fail_silently=fail_silently, auth_user=auth_user,
        auth_password=auth_password, connection=connection, html_message=html_message)


def server_send_mail(
        subject,
        message,
        recipient_list,
        fail_silently=False,
        connection=None,
        html_message=None, ):
    auth_user = settings.EMAIL_HOST_USER
    from_email = auth_user
    auth_password = settings.EMAIL_HOST_PASSWORD
    return send_mail(
        subject, message, from_email, recipient_list, fail_silently=fail_silently, auth_user=auth_user,
        auth_password=auth_password, connection=connection, html_message=html_message)


@handle_send_mail
def send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    return _send_mass_mail(
        datatuple, fail_silently=fail_silently, auth_user=auth_user, auth_password=auth_password, connection=connection)


def server_send_mass_mail(datatuple, fail_silently=False, connection=None):
    auth_user = settings.EMAIL_HOST_USER,
    auth_password = settings.EMAIL_HOST_PASSWORD,
    return send_mass_mail(
        datatuple, fail_silently=fail_silently, auth_user=auth_user, auth_password=auth_password, connection=connection)


@handle_send_mail
def mail_admins(subject, message, fail_silently=False, connection=None, html_message=None):
    return _mail_admins(subject, message, fail_silently=fail_silently, connection=connection, html_message=html_message)


@handle_send_mail
def mail_managers(subject, message, fail_silently=False, connection=None, html_message=None):
    return _mail_managers(
        subject, message, fail_silently=fail_silently, connection=connection, html_message=html_message)
