# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/15 23:47
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

from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import FileUploadSuccess
from Common.viewModels.project import handle_upload_project_report
from Sample.utils.forms.tgfbi import TGFBIReportForm
from Sample.viewModels.tgfbi import decrypt_tgfbi_text


class TGFBISampleLIMSUpdateReportAPIView(AllowAnyAPIView):
    def post(self, request, *args, **kwargs):
        form = TGFBIReportForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ParameterError(chinese_msg='数据格式错误', msg_detail=form.errors)
        project = decrypt_tgfbi_text(form.cleaned_data['encrypted_text'])
        if not project:
            raise ParameterError('加密字段验证错误')
        handle_upload_project_report(project, form.cleaned_data['report_file'])
        return Response(FileUploadSuccess(chinese_msg='上传文件成功'))
