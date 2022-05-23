# -*- encoding: utf-8 -*-
"""
@File Name      :   init_data.py    
@Create Time    :   2022/4/7 16:00
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
from datetime import datetime

import pandas as pd
from django.contrib.auth.models import Group, Permission, ContentType
from django.core.management.base import BaseCommand
from django.db.models import Q

from Common.models.equipments import *
from Common.models.role import *
from Common.models.user import User
from Common.utils.file_handler import validate_file_path
from Common.utils.time import print_accurate_execute_time, create_tz_time
from Common.viewModels.project import update_or_create_project_data
from UserService.models.user import Feedback


@print_accurate_execute_time
def init_permission():
    print('初始化权限完毕')


@print_accurate_execute_time
def init_group():
    admin_group, admin_group_created = Group.objects.get_or_create(name='admin')
    if admin_group_created:
        content_types = ContentType.objects.filter(app_label__in=['Common', 'Screening', 'UserService'])
        permissions = Permission.objects.filter(content_type__in=content_types)
        admin_group.permissions.add(*permissions)
    manager_group, manager_group_created = Group.objects.get_or_create(name='manager')
    if manager_group_created:
        content_types = ContentType.objects.get_for_models(
            User, Employee, Student, Teacher, WeChat, QQ, Weibo,
            Project, VisualChart, Optometry, TonoMeter, EyeGround, Sequence, InformedConsent, Questionnaire,
            Feedback
        ).values()
        permissions = Permission.objects.filter(content_type__in=content_types).exclude(codename__icontains='delete')
        manager_group.permissions.add(*permissions)

    employee_group, employee_group_created = Group.objects.get_or_create(name='employee')
    if employee_group_created:
        project_content_types = ContentType.objects.get_for_models(
            Project, VisualChart, Optometry, TonoMeter,  Sequence,
        ).values()
        project_permissions = Permission.objects.filter(content_type__in=project_content_types).exclude(
            codename__icontains='delete'
        )
        employee_group.permissions.add(*project_permissions)
        user_role_content_types = ContentType.objects.get_for_models(User, Student, Teacher, WeChat, QQ, Weibo).values()
        user_role_permissions = Permission.objects.filter(content_type__in=user_role_content_types).filter(
            codename__icontains='view')
        employee_group.permissions.add(*user_role_permissions)
    normal_user_group, normal_user_group_created = Group.objects.get_or_create(name='user')
    if normal_user_group_created:
        project_content_types = ContentType.objects.get_for_models(
            Project, VisualChart, BioMeter, Optometry, TonoMeter, EyeGround, Sequence, InformedConsent, Questionnaire
        ).values()
        project_permissions = Permission.objects.filter(content_type__in=project_content_types).filter(
            codename__icontains='view')
        normal_user_group.permissions.add(*project_permissions)
        user_role_content_types = ContentType.objects.get_for_models(User, Student, Teacher, WeChat, QQ, Weibo).values()
        user_role_permissions = Permission.objects.filter(content_type__in=user_role_content_types)
        normal_user_group.permissions.add(*user_role_permissions)
    print('初始化用户组完毕')


@print_accurate_execute_time
def init_user():
    # 超级用户账号
    if not User.objects.filter(username='diklios').exists():
        superuser = User.objects.create_superuser(username='diklios', password='laobatai981218')
    # 拥有者账号
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_admin_user(username='admin', password='wmu-admin')
    else:
        admin_user = User.objects.get(username='admin')
    if not admin_user.groups.filter(name='admin').exists():
        admin_group = Group.objects.get(name='admin')
        admin_user.groups.add(admin_group)
    # 管理员账号
    if not User.objects.filter(username='manager').exists():
        manager_user = User.objects.create_user(username='manager', password='wmu-manager')
    else:
        manager_user = User.objects.get(username='manager')
    Manager.objects.get_or_create(user=manager_user)
    if not manager_user.groups.filter(name='manager').exists():
        manager_group = Group.objects.get(name='manager')
        manager_user.groups.add(manager_group)
    # 员工账号
    if not User.objects.filter(username='employee-test').exists():
        employee_user = User.objects.create_user(username='employee-test', password='wmu-employee-test')
    else:
        employee_user = User.objects.get(username='employee-test')
    Employee.objects.get_or_create(user=employee_user)
    if not employee_user.groups.filter(name='employee').exists():
        employee_group = Group.objects.get(name='employee')
        employee_user.groups.add(employee_group)
    # 普通用户账号
    if not User.objects.filter(username='test').exists():
        test_normal_user = User.objects.create_user(username='test', password='wmu-test')
    else:
        test_normal_user = User.objects.get(username='test')
    if not test_normal_user.groups.filter(name='user').exists():
        normal_user_group = Group.objects.get(name='user')
        test_normal_user.groups.add(normal_user_group)
    print('初始化用户完毕')


@print_accurate_execute_time
def init():
    init_permission()
    init_group()
    init_user()
    print('初始化完毕')


# 暂时不想写批量导入数据的方法，因为数据量不是很大
@print_accurate_execute_time
def import_student_sampling_data(file_path: str):
    if not validate_file_path(file_path):
        return False
    df = pd.read_excel(file_path, sheet_name='Students', engine='openpyxl', dtype={"学籍号": str})
    # 解决MySQL数据库nan提交不了的问题
    df = df.astype(object).where(pd.notnull(df), None)
    for index, row in df.iterrows():
        print(index)
        try:
            user = User.objects.get(username=row['学籍号'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=row['学籍号'],
                name=row['学生名称'],
                identification_card_type=1,
                identification_card_number=row['证件号'],
                gender=1 if row['性别'] == '男' else 2
            )
        normal_user_group = Group.objects.get(name='user')
        user.groups.add(normal_user_group)
        Student.objects.update_or_create(
            user=user,
            defaults={
                'student_number': row['学籍号'],
                'student_type': row.get('学生类型', 5),
                'grade': str(row['学籍号'])[:2] + '级',
                'PE_classname': row['班级名称']
            })
        project, project_created = Project.objects.update_or_create(
            user=user,
            defaults={
                'name': '2022-温医大-茶山校区-大学生',
                'progress': 1,
                # 没法用isnull()或者isna()方法来判断
                'finished_time': create_tz_time(datetime.strptime(str(row['创建时间']), '%Y-%m-%d %H:%M:%S'))
                if row['创建时间'] is not pd.NaT and row['创建时间'] is not None else None,
            }
        )
        update_or_create_project_data(project, row)


# todo:待完善用户和教师的数据导入和数据补充
@print_accurate_execute_time
def supply_student_info(file_path: str):
    pass


@print_accurate_execute_time
def import_teacher_sampling_data(file_path: str):
    if not validate_file_path(file_path):
        return False
    df = pd.read_excel(file_path, sheet_name='Teachers', engine='openpyxl', dtype={"教工号": str})
    df = df.astype(object).where(pd.notnull(df), None)
    for index, row in df.iterrows():
        print(index)
        try:
            user = User.objects.get(username=row['教工号'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=row['教工号'],
                name=row['教师名称']
            )
        normal_user_group = Group.objects.get(name='user')
        user.groups.add(normal_user_group)
        Teacher.objects.update_or_create(
            user=user,
            defaults={
                'teacher_number': row['教工号']
            }
        )
        project, project_created = Project.objects.update_or_create(
            user=user,
            defaults={
                'name': '2022-温医大-茶山校区-教职工',
                'progress': 1,
                'finished_time': create_tz_time(datetime.strptime(str(row['创建时间']), '%Y-%m-%d %H:%M:%S'))
                if row['创建时间'] is not pd.NaT and row['创建时间'] is not None else None,
            }
        )
        update_or_create_project_data(project, row)


@print_accurate_execute_time
def supply_teacher_info(file_path: str):
    pass


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-i', '--init', action='store_true', help='init data')
        parser.add_argument('-p', '--permission', action='store_true', help='init permission data')
        parser.add_argument('-g', '--group', action='store_true', help='init group data')
        parser.add_argument('-u', '--user', action='store_true', help='init user data')
        parser.add_argument('-S', '--student_sampling', action='store_true', help='import students\' sampling data')
        parser.add_argument('-T', '--teacher_sampling', action='store_true', help='import teachers\' sampling data')
        parser.add_argument('-SS', '--student_supplement', action='store_true', help='supply students\' data')
        parser.add_argument('-ST', '--teacher_supplement', action='store_true', help='supply teachers\' data')
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')

    def handle(self, *args, **options):
        file_path = options.get('file_path', None)
        if options.get('init', None):
            init()
        elif options.get('permission', None):
            init_permission()
        elif options.get('group', None):
            init_group()
        elif options.get('user', None):
            init_user()
        elif options.get('student_sampling', None):
            import_student_sampling_data(file_path)
        elif options.get('teacher_sampling', None):
            import_teacher_sampling_data(file_path)
        elif options.get('student_supplement', None):
            supply_student_info(file_path)
        elif options.get('teacher_supplement', None):
            supply_teacher_info(file_path)
        else:
            print('-u or -g or -p or -s is required')
