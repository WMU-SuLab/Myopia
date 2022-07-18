# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
@Create Time    :   2022/6/30 11:36
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

from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.shortcuts import redirect
from rest_framework.response import Response

from Common.models.project import Project
from Common.models.user import User
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.exceptions import AuthenticationFailed, PermissionDenied, ParameterError
from Common.utils.http.successes import Success, FileUploadSuccess
from Common.viewModels.project import handle_upload_project_report
from UserService.utils.auth.views import sample_manager_redirect_field_name
from UserService.utils.auth.views.api import SampleManagerIsAuthenticatedAPIView
from UserService.utils.forms.sample import SampleManageForm


class SampleManagerLoginAPIView(AllowAnyAPIView):
    def post(self, request):
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')
        next_url = request.POST.get(sample_manager_redirect_field_name, 'UserService:web:sample_manager_index')
        if not username or not password:
            return Response(ParameterError())
        user: User = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name='sample_manager'):
                login(request, user)
                return redirect(next_url)
            else:
                return Response(PermissionDenied())
        else:
            return Response(AuthenticationFailed(message='用户名或密码错误'))


class SampleManagerLogoutAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        logout(request)
        return redirect('UserService:web:sample_manager_login')


class SampleUserProjectsAPIView(SampleManagerIsAuthenticatedAPIView):
    def get(self, request):
        projects = Project.objects.filter(name='用户自采样')
        count = projects.count()
        # 过滤
        serial_number = request.GET.get('serial_number', '')
        if serial_number:
            projects = projects.filter(sequence__serial_number__contains=serial_number)
        name = request.GET.get('name', '')
        if name:
            projects = projects.annotate(remarks_json_name=F('remarks_json__name')).filter(
                remarks_json_name__icontains=name)
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        projects = projects.order_by('-id')[(int(page) - 1) * int(limit):int(page) * int(limit)]
        projects = projects.prefetch_related('sequence')
        rows = [{
            'id': project.id,
            'serial_number': project.sequence.serial_number,
            'name': project.remarks_json.get('name', None),
            'gender': project.remarks_json.get('gender', None),
            'age': project.remarks_json.get('age', None),
            'birthday': project.remarks_json.get('birthday', None),
            'native_place': project.remarks_json.get('native_place', None),
            'contact_phone': project.remarks_json.get('contact_phone', ''),
            'nationality': project.remarks_json.get('nationality', None),
            'education': project.remarks_json.get('education', None),
            'progress': project.get_progress_display(),
            'report_file_name': os.path.basename(project.report_file_path) if project.report_file_path else '无',
        } for project in projects]
        return Response(Success({'count': count, 'rows': rows}))


class SampleProjectUpdateAPIView(SampleManagerIsAuthenticatedAPIView):
    def post(self, request):
        print(request.POST)
        print(request.POST['progress'])
        form = SampleManageForm(request.POST, request.FILES)
        if form.is_valid():
            project = Project.objects.get(id=form.cleaned_data['project_id'])
            project.progress = form.cleaned_data['progress'] or project.progress
            project.save()
            return Response(Success(chinese_msg='更新数据成功'))
        else:
            return Response(ParameterError(msg='form not valid', msg_detail=str(form.errors)))


class SampleProjectUploadReportFileAPIView(SampleManagerIsAuthenticatedAPIView):
    def post(self, request, project_id):
        project_id = request.POST.get('project_id', project_id)
        if not project_id:
            return Response(ParameterError(chinese_msg='项目id不能为空'))
        report_file = request.FILES.get('file', None)
        if not report_file:
            return Response(ParameterError(chinese_msg='上传文件为空'))
        project = Project.objects.get(id=project_id)
        handle_upload_project_report(project, report_file)
        return Response(FileUploadSuccess(chinese_msg='上传文件成功'))
