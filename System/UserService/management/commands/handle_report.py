# -*- encoding: utf-8 -*-
"""
@File Name      :   handle_report.py    
@Create Time    :   2022/4/8 11:09
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

import os
from abc import ABCMeta

import pandas as pd
from PyPDF2 import PdfFileMerger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template.loader import render_to_string
from weasyprint import HTML

from Common.models.project import Project
from Common.viewModels import reverse_choices_to_dict
from Common.viewModels.equipments.optometry import count_spherical_equivalent
from Common.viewModels.project import generate_project_report_filename, generate_report_data_from_project
from Common.viewModels.project import generate_report_suggestions


def generate_reports_from_table(file_path: str):
    """
    示例：python manage.py handle_report -c --file_path=/data/Myopia/System/data/user/csv
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        print('file not exists')
        return
    dir_path = os.path.dirname(file_path)
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, sheet_name='Teacher')
    else:
        raise Exception('file_path must be csv or xlsx')
    df = df.astype(object).where(pd.notnull(df), None)
    for index, row in df.iterrows():
        uncorrected_visual_acuity_right = row['右裸眼视力']
        uncorrected_visual_acuity_left = row['左裸眼视力']
        corrected_visual_acuity_right = row['右矫正视力']
        corrected_visual_acuity_left = row['左矫正视力']

        if not corrected_visual_acuity_right or not corrected_visual_acuity_left:
            if uncorrected_visual_acuity_right and uncorrected_visual_acuity_left:
                corrected_visual_acuity_right = uncorrected_visual_acuity_right
                corrected_visual_acuity_left = uncorrected_visual_acuity_left
            else:
                print(f"{row['姓名']}的视力数据不完整")
                continue
        eye_data = {
            'corrected_visual_acuity_right': corrected_visual_acuity_right,
            'corrected_visual_acuity_left': corrected_visual_acuity_left,

            'intraocular_tension_right': row['右眼眼压'],
            'intraocular_tension_left': row['左眼眼压'],

            'axial_length_right': row['右眼眼轴长度(AL)'],
            'axial_length_left': row['左眼眼轴长度(AL)'],
            'corneal_thickness_right': row['右眼角膜厚度(CCT)'],
            'corneal_thickness_left': row['左眼角膜厚度(CCT)'],

            'spherical_right': row['右球镜s'],
            'spherical_left': row['左球镜s'],
            'column_right': row['右柱镜c'],
            'column_left': row['左柱镜c'],
            'axis_right': row['右轴位a'],
            'axis_left': row['左轴位a'],
            'spherical_equivalent_right': count_spherical_equivalent(row['右球镜s'], row['右柱镜c']),
            'spherical_equivalent_left': count_spherical_equivalent(row['左球镜s'], row['左柱镜c']),
        }
        report_str = render_to_string(
            template_name='UserService/report/single.html',
            context={"user": {
                "name": row['姓名'],
                "gender": row['性别'],
                "age": '无',
                **eye_data,
                'suggestions': generate_report_suggestions(eye_data)
            }})
        HTML(string=report_str).write_pdf(os.path.join(dir_path, f'{row["姓名"]}.pdf'))


def generate_user_reports(divide=False, file_path=None, dir_path=None):
    """
    示例：python manage.py handle_report -g -d --dir_path=/data/Myopia/System/data/user/pdf
    :param divide:
    :param file_path:
    :param dir_path:
    :return:
    """
    projects = Project.objects.all().prefetch_related(
        'user', 'user__student_role', 'visual_chart', 'tono_meter', 'bio_meter', 'optometry')
    if divide:
        for project in projects:
            report_str = render_to_string(
                template_name='UserService/report/single.html',
                context={"user": generate_report_data_from_project(project)})
            HTML(string=report_str).write_pdf(os.path.join(dir_path, generate_project_report_filename(project)))
    else:
        users_report_data = [generate_report_data_from_project(project) for project in projects]
        report_str = render_to_string(template_name='UserService/report/multiple.html',
                                      context={"users": users_report_data})
        HTML(string=report_str).write_pdf(file_path)


def merge_pdf(dir_path):
    """
    示例：python manage.py handle_report -m --dir_path=/data/Myopia/System/data/user/pdf
    :param dir_path:
    :return:
    """
    finished_progress = reverse_choices_to_dict(Project.progress_choices)['已完成']
    for project in Project.objects.filter(progress=finished_progress):
        merger = PdfFileMerger()
        file_path1 = os.path.join(dir_path, generate_project_report_filename(project))
        file_path2 = os.path.join(dir_path, f'{project.user.name}-{project.user.username}.pdf')
        if os.path.exists(file_path1) and os.path.exists(file_path2):
            joint_file_path = os.path.join(dir_path, 'joint-' + generate_project_report_filename(project))
            if project.report_file_path == joint_file_path and os.path.exists(joint_file_path):
                continue
            merger.append(file_path1)
            merger.append(file_path2)
            merger.write(joint_file_path)
            project.report_file_path = joint_file_path
            project.remarks_json['report_file_full'] = True
            project.save()
        elif os.path.exists(file_path1):
            project.report_file_path = file_path1
            project.remarks_json['report_file_full'] = False
            project.save()
        print(f'{file_path1} finished')


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-c', '--clean', action='store_true', help='clean all reports')
        parser.add_argument('-g', '--generate', action='store_true', help='generate users\' reports')
        parser.add_argument('-d', '--divide', action='store_true', help='divide report in different files')
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')
        parser.add_argument('-m', '--merge', action='store_true', help='merge pdf files')
        parser.add_argument('-G', '--GT', action='store_true', help='generate reports from table')
        parser.add_argument('--dir_path', type=str, help='dir path')

    def handle(self, *args, **options):
        if options['clean']:
            Project.objects.filter(
                Q(report_data__isnull=False) | Q(report_file_url__isnull=False) | Q(report_file_path__isnull=False)) \
                .update(report_data=None, report_file_url=None, report_file_path=None)
        elif options['generate']:
            divide = options['divide']
            file_path = options['file_path']
            dir_path = options['dir_path']
            if divide:
                if not dir_path:
                    dir_path = os.path.join(settings.BASE_DIR, 'data', 'user', 'pdf')
                    generate_user_reports(divide=True, dir_path=dir_path)
                else:
                    generate_user_reports(divide=True, dir_path=dir_path)
            else:
                if not file_path:
                    file_path = './reports.pdf'
                    generate_user_reports(divide=False, file_path=file_path)
                else:
                    generate_user_reports(divide=False, file_path=file_path)
        elif options['merge']:
            dir_path = options['dir_path']
            if not dir_path:
                dir_path = os.path.join(settings.BASE_DIR, 'data', 'user', 'pdf')
            merge_pdf(dir_path=dir_path)
        elif options['GT']:
            if not options['file_path']:
                print('请输入文件路径')
                return
            generate_reports_from_table(options['file_path'])
