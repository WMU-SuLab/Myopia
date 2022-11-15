# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py
@Create Time    :   2022/11/13 16:19
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

from rest_framework.response import Response

from Common.utils.auth.views.api import IsAuthenticatedAPIView
from Common.utils.http.exceptions import NotFound
from Common.utils.http.successes import Success
from Sample.models.project import Project, HighMyopiaSampleProject, TGFBISampleProject
from Sample.viewModels.project import get_project_info


class ProjectsListAPIView(IsAuthenticatedAPIView):
    def get(self, request, *args, **kwargs):
        high_myopia_projects = HighMyopiaSampleProject.objects.filter(
            user=request.user, name='高度近视遗传风险评估采样').prefetch_related('sequence')
        high_myopia_projects_data = [get_project_info(project) for project in high_myopia_projects]
        tgfbi_projects = TGFBISampleProject.objects.filter(user=request.user, name='TGFBI角膜营养不良基因检测采样') \
            .prefetch_related('sequence')
        tgfbi_projects_data = [get_project_info(project) for project in tgfbi_projects]
        return Response(Success(data=[*high_myopia_projects_data, *tgfbi_projects_data]))


class ProjectRetrieveAPIView(IsAuthenticatedAPIView):
    def get(self, request, serial_number, *args, **kwargs):
        projects = Project.objects.filter(user=request.user, sequence__serial_number=serial_number)
        if projects.exists() and projects.count() == 1:
            project = projects.first()
            if project.name == '高度近视遗传风险评估采样':
                project = HighMyopiaSampleProject.objects.get(user=request.user, sequence__serial_number=serial_number)
                data = {
                    'serial_number': serial_number,
                    'project_name': project.name,
                    'progress': project.get_progress_display(),
                    'progress_code': project.progress,
                    'user': {
                        'name': project.remarks_json.get('name', None),
                        'gender': project.remarks_json.get('gender', None),
                        'age': project.remarks_json.get('age', None),
                        'birthday': project.remarks_json.get('birthday', None),
                        'native_place': project.remarks_json.get('native_place', None),
                        'contact_phone': project.remarks_json.get('contact_phone', ''),
                        'nationality': project.remarks_json.get('nationality', None),
                        'education': project.remarks_json.get('education', None)
                    },
                    'eye': {
                        'wear_glasses_first_time': project.remarks_json.get('wear_glasses_first_time', None),
                        'optometry_left': project.remarks_json.get('optometry_left', None),
                        'optometry_right': project.remarks_json.get('optometry_right', None),
                        'family_history': project.remarks_json.get('family_history', None),
                    },
                }
            elif project.name == 'TGFBI角膜营养不良基因检测采样':
                project = TGFBISampleProject.objects.get(user=request.user, sequence__serial_number=serial_number)
                data = {
                    'serial_number': serial_number,
                    'project_name': project.name,
                    'progress': project.get_progress_display(),
                    'progress_code': project.progress,
                    'user': {
                        'name': project.remarks_json.get('name', None),
                        'gender': project.remarks_json.get('gender', None),
                        'birthday': project.remarks_json.get('birthday', None),
                        'contact_phone_number': project.remarks_json.get('contact_phone_number', ''),
                        'identification_card_type': project.remarks_json.get('identification_card_type', ''),
                        'identification_card_number': project.remarks_json.get('identification_card_number', ''),
                    },
                    'sample': {
                        'body_part': project.remarks_json.get('body_part', None),
                        'bind_time': project.remarks_json.get('bind_time', None),
                    },
                    'courier': project.remarks_json.get('courier', {}),
                }
            else:
                return Response(NotFound(chinese_msg='虽然编号存在，但是不属于此产品项目'))
            return Response(Success(data=data))
        else:
            return Response(NotFound(chinese_msg='编号不存在'))
