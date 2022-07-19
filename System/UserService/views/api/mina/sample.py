# -*- encoding: utf-8 -*-
"""
@File Name      :   sampling.py    
@Create Time    :   2022/5/26 21:56
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

from django.conf import settings
from django.utils.timezone import localtime, get_current_timezone_name
from rest_framework.response import Response

from Common.models.equipments import Sequence, InformedConsent
from Common.models.project import Project
from Common.utils.alibabacloud.oss.obj import upload_obj, generate_obj_file_path
from Common.utils.alibabacloud.oss.url import generate_file_url, generate_image_url
from Common.utils.alibabacloud.sms.verification import send_verification_sms
from Common.utils.auth.views.api import IsAuthenticatedAPIView
from Common.utils.file_handler import handle_upload_file, rename_file
from Common.utils.file_handler.image_handler import is_image_file
from Common.utils.http.exceptions import NotFound, ParameterError, MethodNotAllowed
from Common.utils.http.successes import Success, PhoneSMSSendSuccess
from Common.viewModels.equipments.informed_consent import generate_project_informed_consent_file_name
from Common.viewModels.equipments.informed_consent import handle_upload_informed_consent
from Common.views.api.user import SendPhoneSMSAPIView as _SendPhoneSMSAPIView
from UserService.utils.forms.sample import SampleForm, SampleFormUpdate


class SendPhoneSMSAPIView(_SendPhoneSMSAPIView):
    def post(self, request):
        usage = request.GET.get('usage', None)
        if not usage:
            raise ParameterError(msg_detail='usage field is required')
        data = send_verification_sms(self.validate(request), '谱希基因', 'SMS_244615604', usage)
        return Response(PhoneSMSSendSuccess(data=data))


class SerialNumberList(IsAuthenticatedAPIView):
    def get(self, request, *args, **kwargs):
        """
        获取自采样的序列号列表
        """
        sequences = [{
            'serial_number': sequence.serial_number,
            'name': sequence.project.remarks_json.get('name', None),
            'progress': sequence.project.get_progress_display(),
            # 数据库中取出来的是UTC时间
            'created_time': localtime(sequence.created_time).strftime('%Y-%m-%d %H:%M:%S'),
            'tzname': get_current_timezone_name(),
            # 但是不知道为什么timestamp是本地时间
            'created_time_timestamp': sequence.created_time.timestamp(),
            'report_file_url': generate_file_url(sequence.project.report_file_url, sequence.project.report_file_path),
        } for sequence in Sequence.objects.filter(project__user=request.user)]
        return Response(Success(data=sequences))


class SerialNumberRetrieve(IsAuthenticatedAPIView):
    def get(self, request, serial_number, *args, **kwargs):
        sequence = Sequence.objects.filter(serial_number=serial_number)
        if sequence.exists():
            sequence = sequence.first()
            project = sequence.project
            data = {
                'serial_number': serial_number,
                'progress': project.get_progress_display(),
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
                'informed_consent': generate_image_url(
                    image_url=project.informed_consent.file_url,
                    image_path=project.informed_consent.file_path
                ),
            }
            return Response(Success(data=data))
        else:
            return Response(NotFound(chinese_msg='序列号不存在'))


class SubmitSampleForm(IsAuthenticatedAPIView):
    def create(self, request, *args, **kwargs):
        sample_form = SampleForm(request.POST, request.FILES)
        if not sample_form.is_valid():
            return Response(ParameterError(msg_detail=str(sample_form.errors)))
        serial_number = sample_form.cleaned_data['serial_number']
        if Sequence.objects.filter(serial_number=serial_number).exists():
            return Response(MethodNotAllowed(chinese_msg='序列号已存在，不允许使用此方法'))
        # 处理知情同意书
        informed_consent_file = sample_form.cleaned_data.pop('informed_consent_file')
        if not informed_consent_file:
            return Response(ParameterError(chinese_msg='请上传同意书'))
        project = Project.objects.create(
            user=request.user,
            name='用户自采样',
            progress=1,
            remarks_json=sample_form.cleaned_data,
        )
        Sequence.objects.create(project=project, serial_number=serial_number)
        # 上传到本地文件
        informed_consent_dir_path = settings.INFORMED_CONSENT_DIR_PATH
        informed_consent_file_path = os.path.join(informed_consent_dir_path, informed_consent_file.name)
        handle_upload_file(informed_consent_file, informed_consent_file_path)
        if not is_image_file(informed_consent_file_path):
            return Response(ParameterError(chinese_msg='上传的不是图片文件'))
        # 重命名为规范的文件名
        informed_consent = InformedConsent.objects.create(project=project)
        informed_consent_new_file_name = generate_project_informed_consent_file_name(
            informed_consent, file_type=informed_consent_file.name.split('.')[-1])
        informed_consent_new_file_path = os.path.join(informed_consent_dir_path, informed_consent_new_file_name)
        rename_file(informed_consent_file_path, informed_consent_new_file_path)
        informed_consent.file_path = informed_consent_new_file_path
        # 上传OSS
        informed_consent_file_obj_name = os.path.join(settings.RELATIVE_INFORMED_CONSENT_DIR_PATH,
                                                      informed_consent_new_file_name)
        upload_obj(informed_consent_file_obj_name, informed_consent_new_file_path)
        informed_consent.file_url = generate_obj_file_path(informed_consent_file_obj_name)
        informed_consent.full_clean(exclude=['file_url'],validate_unique=True)
        informed_consent.save()
        return Response(Success(chinese_msg='提交成功'))

    def post(self, request, *args, **kwargs):
        update_type = request.POST.get('update_type', None)
        if update_type and update_type in ['pat', 'patch', 'PAT', 'PATCH']:
            request.method = 'PATCH'
            return self.patch(request, *args, **kwargs)
        else:
            return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        sample_form = SampleFormUpdate(request.POST, request.FILES)
        if not sample_form.is_valid():
            return Response(ParameterError(msg='form not valid', msg_detail=str(sample_form.errors)))
        sequence = Sequence.objects.filter(serial_number=sample_form.cleaned_data['serial_number'])
        if not sequence.exists():
            return Response(ParameterError(chinese_msg='序列号不存在'))
        sequence = sequence.first()
        project = sequence.project
        # 判断用户
        if project.user.username != request.user.username:
            return Response(ParameterError(chinese_msg='该序列号不属于当前用户'))
        # 判断是否更新图片
        informed_consent_file = sample_form.cleaned_data.pop('informed_consent_file')
        if informed_consent_file:
            handle_upload_informed_consent(project, informed_consent_file)
        # 简便写法
        project.remarks_json = {**project.remarks_json,**sample_form.cleaned_data }
        project.full_clean(exclude=['report_file_url'], validate_unique=True)
        project.save()
        return Response(Success(chinese_msg='更新成功'))
