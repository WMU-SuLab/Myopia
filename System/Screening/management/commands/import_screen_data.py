# -*- encoding: utf-8 -*-
"""
@File Name      :   import_screen_data.py
@Create Time    :   2022/12/1 20:29
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
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from Common.libs.choices import common_progress_choices
from Common.models.project import Project
from Common.models.role import *
from Common.utils.file_handler.file import validate_file_path
from Common.utils.time import print_accurate_execute_time, create_tz_time
from Common.viewModels.choices import reverse_choices_to_dict
from Common.viewModels.project import update_or_create_project_data


# 暂时不想写批量导入数据的方法，因为数据量不是很大
@print_accurate_execute_time
def import_student_sampling_data(file_path: str):
    if not validate_file_path(file_path):
        return False
    df = pd.read_excel(file_path, sheet_name='Students', engine='openpyxl', dtype={"学籍号": str})
    # 解决MySQL数据库nan提交不了的问题
    df = df.astype(object).where(pd.notnull(df), None)
    student_type = reverse_choices_to_dict(student_type_choices)['大学生']
    finished_progress = reverse_choices_to_dict(common_progress_choices)['已完成']
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
                'student_type': student_type,
                'grade': str(row['学籍号'])[:2] + '级',
                'PE_classname': row['班级名称']
            })
        project, project_created = Project.objects.update_or_create(
            user=user,
            defaults={
                'name': row['项目名称'],
                'progress': finished_progress,
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
        parser.add_argument('-S', '--student_sampling', action='store_true', help="import students' sampling data")
        parser.add_argument('-SS', '--student_supplement', action='store_true', help="supply students' data")
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')

    def handle(self, *args, **options):
        file_path = options.get('file_path', None)
        if options.get('student_sampling', None):
            import_student_sampling_data(file_path)
        elif options.get('student_supplement', None):
            supply_student_info(file_path)
        else:
            print('-u or -g or -p or -s is required')
