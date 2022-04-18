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
from django.conf import settings
from django.core.management.base import BaseCommand

from Common.models.equipments import *
from Common.models.role import Student, Teacher
from Common.models.user import User
from Common.utils.file_handler import validate_file_path
from Common.utils.time import print_accurate_execute_time
from Common.viewModels.project import update_or_create_project_data


@print_accurate_execute_time
def init_user():
    pass


@print_accurate_execute_time
def init_group():
    pass


@print_accurate_execute_time
def init_permission():
    pass


# 暂时不想写批量导入数据的方法，因为数据量不是很大
@print_accurate_execute_time
def import_student_sampling_data(file_path: str):
    if not validate_file_path(file_path):
        return False
    df = pd.read_excel(file_path, sheet_name='温医大学生结果导出0414', engine='openpyxl', dtype={"学籍号": str})
    # 解决MySQL数据库nan提交不了的问题
    df= df.astype(object).where(pd.notnull(df), None)
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
        Student.objects.update_or_create(
            user=user,
            defaults={
                'student_number': row['学籍号'],
                'grade': str(row['学籍号'])[:2] + '级',
                'PE_classname': row['班级名称']
            })
        project, project_created = Project.objects.update_or_create(
            user=user,
            defaults={
                'name': '22年温医大茶山校区大学生眼健康筛查项目',
                'is_finished': True,
                # 没法用isnull()或者isna()方法来判断
                'finished_time': datetime.strptime(str(row['创建时间']), '%Y-%m-%d %H:%M:%S').astimezone(
                    settings.TZ_INFO) if row['创建时间'] is not pd.NaT and row['创建时间'] is not None else None,
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
    df = pd.read_excel(file_path, sheet_name='Sheet1', engine='openpyxl')
    df = df.astype(object).where(pd.notnull(df), None)
    for index, row in df.iterrows():
        try:
            user = User.objects.get(username=row['教工号'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=row['教工号'],
                name=row['教师名称']
            )
        Teacher.objects.update_or_create(
            user=user,
            defaults={
                'teacher_number': row['教工号']
            }
        )
        project, project_created = Project.objects.update_or_create(
            user=user,
            defaults={
                'name': '22年温医大茶山校区大学生眼健康筛查项目-教师',
                'is_finished': True,
                'finished_time': datetime.strptime(str(row['创建时间']), '%Y-%m-%d %H:%M:%S').astimezone(
                    settings.TZ_INFO) if row['创建时间'] is not pd.NaT and row['创建时间'] is not None else None,
            }
        )
        update_or_create_project_data(project, row)


@print_accurate_execute_time
def supply_teacher_info(file_path: str):
    pass


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', action='store_true', help='init user data')
        parser.add_argument('-g', '--group', action='store_true', help='init group data')
        parser.add_argument('-p', '--permission', action='store_true', help='init permission data')
        parser.add_argument('-S', '--student_sampling', action='store_true', help='import students\' sampling data')
        parser.add_argument('-T', '--teacher_sampling', action='store_true', help='import teachers\' sampling data')
        parser.add_argument('-SS', '--student_supplement', action='store_true', help='supply students\' data')
        parser.add_argument('-ST', '--teacher_supplement', action='store_true', help='supply teachers\' data')
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')

    def handle(self, *args, **options):
        file_path = options.get('file_path', None)
        if options.get('user', None):
            init_user()
        elif options.get('group', None):
            init_group()
        elif options.get('permission', None):
            init_permission()
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
