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

import json
import os
from abc import ABCMeta
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.contrib.auth.models import Group, Permission, ContentType
from django.core.management.base import BaseCommand

from Common.models.equipments import *
from Common.models.regions import Country, Province, City, Area, Street
from Common.models.role import *
from Common.models.user import User, Nationality
from Common.utils.file_handler import validate_file_path
from Common.utils.file_handler.dir import make_dir
from Common.utils.time import print_accurate_execute_time, create_tz_time
from Common.viewModels.project import update_or_create_project_data
from UserService.models.user import Feedback


@print_accurate_execute_time
def init_dirs():
    for dir_path in settings.DATA_DIR_PATH_LIST + settings.LOGS_DIR_PATH_LIST:
        make_dir(dir_path)
    print('初始化目录完成')


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
            Project, VisualChart, Optometry, TonoMeter, Sequence,
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
    if not User.objects.filter(username='superuser').exists():
        superuser = User.objects.create_superuser(username='superuser', password='wmu-myopia-superuser')
    if not User.objects.filter(username='diklios').exists():
        diklios = User.objects.create_superuser(username='diklios', password='laobatai981218')
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
    if not User.objects.filter(username='normal-user-test').exists():
        test_normal_user = User.objects.create_user(username='normal-user-test', password='wmu-normal-user-test')
    else:
        test_normal_user = User.objects.get(username='normal-user-test')
    if not test_normal_user.groups.filter(name='user').exists():
        normal_user_group = Group.objects.get(name='user')
        test_normal_user.groups.add(normal_user_group)
    print('初始化用户完毕')


@print_accurate_execute_time
def init_regions():
    china, china_created = Country.objects.get_or_create(name='中国')
    china_regions_dir_path = os.path.join(settings.IMPORT_JSON_DATA_DIR_PATH, 'china', 'regions')
    china_province_json_path = os.path.join(china_regions_dir_path, 'province.json')
    if not os.path.exists(china_province_json_path):
        print('china_province.json文件不存在')
        return
    with open(china_province_json_path, 'r', encoding='utf8') as f:
        china_province_json: list = json.load(f)
    Province.objects.bulk_create([Province(id=province['id'], country_id=china.id, name=province['name'])
                                  for province in china_province_json], ignore_conflicts=True)
    print('初始化省份完毕')
    china_city_json_path = os.path.join(china_regions_dir_path, 'city.json')
    if not os.path.exists(china_city_json_path):
        print('china_city.json文件不存在')
        return
    with open(china_city_json_path, 'r', encoding='utf8') as f:
        china_city_json: dict = json.load(f)
    City.objects.bulk_create([City(id=city['id'], province_id=province_id, name=city['name'])
                              for province_id, cities in china_city_json.items()
                              for city in cities], ignore_conflicts=True)
    print('初始化城市完毕')
    china_area_json_path = os.path.join(china_regions_dir_path, 'area.json')
    if not os.path.exists(china_area_json_path):
        print('china_area.json文件不存在')
        return
    with open(china_area_json_path, 'r', encoding='utf8') as f:
        china_area_json: dict = json.load(f)
    Area.objects.bulk_create([Area(id=area['id'], city_id=city_id, name=area['name'])
                              for city_id, areas in china_area_json.items()
                              for area in areas], ignore_conflicts=True)
    print('初始化区域完毕')
    china_street_json_path = os.path.join(china_regions_dir_path, 'street.json')
    if not os.path.exists(china_street_json_path):
        print('china_street.json文件不存在')
        return
    with open(china_street_json_path, 'r', encoding='utf8') as f:
        china_street_json: dict = json.load(f)
    Street.objects.bulk_create([Street(id=street['id'], area_id=area_id, name=street['name'])
                                for area_id, streets in china_street_json.items()
                                for street in streets], ignore_conflicts=True)
    print('初始化街道完毕')


@print_accurate_execute_time
def init_info():
    nationalities_json_path = os.path.join(settings.IMPORT_JSON_DATA_DIR_PATH, 'china', 'nationalities.json')
    with open(nationalities_json_path, 'r', encoding='utf8') as f:
        nationalities_json: list = json.load(f)
        Nationality.objects.bulk_create([Nationality(name=nationality['name'], pinyin=nationality['pinyin'])
                                         for nationality in nationalities_json], ignore_conflicts=True)
    print('初始化民族完毕')


@print_accurate_execute_time
def init():
    init_dirs()
    init_permission()
    init_group()
    init_user()
    init_regions()
    init_info()
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
                'name': row['项目名称'],
                'progress': 5,
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


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-i', '--init', action='store_true', help='init data')
        parser.add_argument('-d', '--dirs', action='store_true', help='init dirs')
        parser.add_argument('-p', '--permission', action='store_true', help='init permission data')
        parser.add_argument('-g', '--group', action='store_true', help='init group data')
        parser.add_argument('-u', '--user', action='store_true', help='init user data')
        parser.add_argument('-r', '--regions', action='store_true', help='init regions data')
        parser.add_argument('-I', '--info', action='store_true', help='init info data')
        parser.add_argument('-S', '--student_sampling', action='store_true', help='import students\' sampling data')
        parser.add_argument('-SS', '--student_supplement', action='store_true', help='supply students\' data')
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')

    def handle(self, *args, **options):
        file_path = options.get('file_path', None)
        if options.get('init', None):
            init()
        elif options.get('dirs', None):
            init_dirs()
        elif options.get('permission', None):
            init_permission()
        elif options.get('group', None):
            init_group()
        elif options.get('user', None):
            init_user()
        elif options.get('regions', None):
            init_regions()
        elif options.get('info', None):
            init_info()
        elif options.get('student_sampling', None):
            import_student_sampling_data(file_path)
        elif options.get('student_supplement', None):
            supply_student_info(file_path)
        else:
            print('-u or -g or -p or -s is required')
