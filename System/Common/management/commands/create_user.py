# -*- encoding: utf-8 -*-
"""
@File Name      :   create_user.py    
@Create Time    :   2022/4/28 8:59
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

from abc import ABCMeta
from secrets import compare_digest

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from Common.models.role import Manager, Employee
from Common.models.user import User


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, required=True, help='init username')
        parser.add_argument('-p1', '--password', type=str, help='password')
        parser.add_argument('-p2', '--confirm_password', type=str, help='confirm password')
        parser.add_argument('-e', '--email', type=str, help='email')
        parser.add_argument('-p', '--phone', type=str, help='phone')
        parser.add_argument('-a', '--admin', action='store_true', help='admin role')
        parser.add_argument('-m', '--manage', action='store_true', help='manage role')
        parser.add_argument('-em', '--employee', action='store_true', help='employee role')

    def handle(self, *args, **options):
        username = options.get('username')
        password = options.get('password', None)
        confirm_password = options.get('confirm_password', None)
        if password:
            if not confirm_password:
                print('please input password again')
                return
            if compare_digest(password, confirm_password):
                print('password not equal')
                return
        email = options.get('email', None)
        phone = options.get('phone', None)
        if options.get('admin', False):
            user = User.objects.create_admin_user(username=username, password=password, email=email, phone=phone)
            admin_group = Group.objects.get(name='admin')
            user.groups.add(admin_group)
        else:
            user = User.objects.create_user(username=username, password=password, email=email, phone=phone)
        if options.get('manage', False):
            Manager.objects.create(user=user)
            manage_group = Group.objects.get(name='manage')
            user.groups.add(manage_group)
        if options.get('employee', False):
            Employee.objects.create(user=user)
            employee_group = Group.objects.get(name='employee')
            user.groups.add(employee_group)
        print('create user success')
