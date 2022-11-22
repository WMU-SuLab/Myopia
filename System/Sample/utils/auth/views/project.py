# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py
@Create Time    :   2022/11/22 21:28
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

from Common.models.project import Project
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import FileUploadSuccess
from Common.viewModels.project import handle_upload_project_report
from .api import SampleManagerIsAuthenticatedAPIView


class ProjectUploadReportFileAPIView(SampleManagerIsAuthenticatedAPIView):
    project_class = Project

    def after_post(self, project: project_class):
        pass

    def post(self, request, project_id):
        project_id = request.POST.get('project_id', project_id)
        if not project_id:
            return Response(ParameterError(chinese_msg='项目id不能为空'))
        report_file = request.FILES.get('file', None)
        if not report_file:
            return Response(ParameterError(chinese_msg='上传文件为空'))
        project = self.project_class.objects.get(id=project_id)
        handle_upload_project_report(project, report_file)
        self.after_post(project)
        return Response(FileUploadSuccess(chinese_msg='上传文件成功'))
