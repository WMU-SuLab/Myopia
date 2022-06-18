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

from PyPDF2 import PdfFileMerger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.template.loader import render_to_string
from weasyprint import HTML

from Common.models.project import Project
from Common.viewModels.project import generate_project_report_filename, generate_report_data_from_project


def generate_user_reports(divide=False, file_path=None, dir_path=None):
    projects = Project.objects.all().prefetch_related(
        'user', 'user__student_role', 'visual_chart', 'tono_meter', 'bio_meter', 'optometry')
    if divide:
        for project in projects:
            report_str = render_to_string(
                template_name='UserService/report/single.html', context=generate_report_data_from_project(project))
            HTML(string=report_str).write_pdf(os.path.join(dir_path, generate_project_report_filename(project)))
    else:
        users_report_data = [generate_report_data_from_project(project) for project in projects]
        report_str = render_to_string(template_name='UserService/report/multiple.html', context=users_report_data)
        HTML(string=report_str).write_pdf(file_path)


def merge_pdf(dir_path):
    for project in Project.objects.filter(is_finished=True):
        merger = PdfFileMerger()
        file_path1 = os.path.join(dir_path, generate_project_report_filename(project))
        file_path2 = os.path.join(dir_path, f'{project.user.name}-{project.user.username}.pdf')
        if os.path.exists(file_path1) and os.path.exists(file_path2):
            joint_file_path = os.path.join(dir_path, 'joint-' + generate_project_report_filename(project))
            if project.report_file_path==joint_file_path and os.path.exists(joint_file_path):
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


class Command(BaseCommand, metaclass=ABCMeta):
    def add_arguments(self, parser):
        parser.add_argument('-c', '--clean', action='store_true', help='clean all reports')
        parser.add_argument('-g', '--generate', action='store_true', help='generate users\' reports')
        parser.add_argument('-d', '--divide', action='store_true', help='divide report in different files')
        parser.add_argument('-f', '--file_path', type=str, help='import data file path')
        parser.add_argument('-m', '--merge', action='store_true', help='merge pdf files')
        parser.add_argument('--dir_path', type=str, help='dir path')

    def handle(self, *args, **options):
        if options['clean']:
            Project.objects.filter(
                Q(report_data__isnull=False) | Q(report_file_url__isnull=False) | Q(report_file_path__isnull=False)) \
                .update(report_data=None, report_file_url=None, report_file_path=None)
        elif options['generate']:
            file_path = options['file_path']
            divide = options['divide']
            dir_path = options['dir_path']
            if divide:
                if not file_path:
                    file_path = './reports.pdf'
                    generate_user_reports(divide=False, file_path=file_path)
                else:
                    generate_user_reports(divide=options['divide'], file_path=file_path)
            else:
                if not dir_path:
                    dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
                    generate_user_reports(divide=True, dir_path=dir_path)
                else:
                    generate_user_reports(divide=True, dir_path=dir_path)
        elif options['merge']:
            dir_path = options['dir_path']
            if not dir_path:
                dir_path = os.path.join(settings.BASE_DIR, 'Common', 'libs', 'pdf')
            merge_pdf(dir_path=dir_path)
