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
from django.urls import reverse
from rest_framework.response import Response

from Common.models.equipments import Sequence, InformedConsent
from Common.models.project import Project
from Common.models.user import User, Nationality
from Common.utils.auth.views.api import IsAuthenticatedAPIView
from Common.utils.file_handler import handle_uploaded_file, remove_file, rename_file
from Common.utils.file_handler.image_handler import is_image_file
from Common.utils.http.exceptions import NotFound, ParameterError, MethodNotAllowed, Conflict
from Common.utils.http.successes import Success
from Common.utils.text_handler.hash import encrypt_text
from Common.viewModels import get_choices_key
from Common.viewModels.equipments.informed_consent import generate_project_informed_consent_file_name
from UserService.utils.forms.sample import SampleForm


class SerialNumberList(IsAuthenticatedAPIView):
    def get(self, request):
        """
        获取自采样的序列号列表
        """
        sequences = [sequence.serial_number for sequence in Sequence.objects.filter(project__user=request.user)]
        return Response(Success(data=sequences))


class SerialNumberRetrieve(IsAuthenticatedAPIView):
    def get(self, request, serial_number, *args, **kwargs):
        sequence = Sequence.objects.filter(serial_number=serial_number)
        if sequence.exists():
            sequence = sequence.first()
            project = sequence.project
            user = project.user

            data = {
                'serial_number': serial_number,
                'project_process': project.get_progress_display(),
                'user': {
                    'name': user.name,
                    'gender': user.get_gender_display(),
                    'age': user.age,
                    'birthday': user.birthday.strftime('%Y-%m-%d'),
                    'native_place': user.native_place,
                    'contact_phone': project.remarks_json.get('contact_phone', ''),
                    'nationality': user.nationality.name,
                    'education': user.get_education_display(),
                },
                'eye': {
                    'wear_glasses_first_time': project.remarks_json.get('wear_glasses_first_time', None),
                    'optometry_left': project.remarks_json.get('optometry_left', None),
                    'optometry_right': project.remarks_json.get('optometry_right', None),
                    'family_history': project.remarks_json.get('family_history', None),
                },
                'informed_consent': reverse('Common:api:download_image', kwargs={
                    'encrypted_file_text': encrypt_text(project.informed_consent.file_path)
                }),

            }
            return Response(Success(data=data))
        else:
            return Response(NotFound(chinese_msg='序列号不存在'))


class SubmitSampleForm(IsAuthenticatedAPIView):
    def set_user_info(self, user, data):
        user.name = data['name']
        user.gender = get_choices_key(User.gender_choices, data['gender'])
        user.age = data['age']
        user.birthday = data['birthday']
        user.native_place = data['native_place']
        user.nationality = Nationality.objects.get(name=data['nationality'])
        user.education = data['education']
        user.save()

    def post(self, request, *args, **kwargs):
        sample_form = SampleForm(request.POST, request.FILES)
        if sample_form.is_valid():
            serial_number = sample_form.cleaned_data['serial_number']
            if Sequence.objects.filter(serial_number=serial_number).exists():
                return Response(MethodNotAllowed(chinese_msg='序列号已存在，不允许使用此方法'))

            user: User = request.user
            self.set_user_info(user, sample_form.cleaned_data)

            project = Project.objects.create(
                user=request.user,
                name='用户自采样',
                progress=1,
                remarks_json={
                    'contact_phone': sample_form.cleaned_data['contact_phone'],
                    'wear_glasses_first_time': sample_form.cleaned_data['wear_glasses_first_time'],
                    'optometry_left': sample_form.cleaned_data['optometry_left'],
                    'optometry_right': sample_form.cleaned_data['optometry_right'],
                    'family_history': sample_form.cleaned_data['family_history'],
                }
            )
            Sequence.objects.create(project=project, serial_number=serial_number)

            informed_consent_file = sample_form.cleaned_data['informed_consent_file']
            if not informed_consent_file:
                return Response(ParameterError(chinese_msg='请上传同意书'))
            informed_consent_dir_path = os.path.join(settings.USER_IMAGES_DATA_DIR_PATH, 'informed_consent')
            informed_consent_file_path = os.path.join(informed_consent_dir_path, informed_consent_file.name)
            if handle_uploaded_file(informed_consent_file, informed_consent_file_path) \
                    and is_image_file(informed_consent_file_path):
                if project.has_informed_consent:
                    raise Conflict(chinese_msg='已经上传过同意书，不允许重复上传')
                informed_consent = InformedConsent.objects.create(project=project)
                informed_consent_new_file_path = os.path.join(
                    informed_consent_dir_path,
                    generate_project_informed_consent_file_name(
                        informed_consent,
                        file_type=informed_consent_file.name.split('.')[-1]))
                if rename_file(informed_consent_file_path, informed_consent_new_file_path):
                    informed_consent.file_path = informed_consent_new_file_path
                    informed_consent.save()
                    return Response(Success(chinese_msg='提交成功'))
                else:
                    return Response(ParameterError(chinese_msg='提交失败'))
            else:
                remove_file(informed_consent_file_path)
                return Response(ParameterError(chinese_msg='上传的不是图片文件'))
        else:
            return Response(ParameterError(msg_detail=str(sample_form.errors)))

    def patch(self, request, *args, **kwargs):
        sample_form = SampleForm(request.POST, request.FILES)
        if sample_form.is_valid():
            sequence = Sequence.objects.filter(serial_number=sample_form.cleaned_data['serial_number'])
            if not sequence.exists():
                return Response(ParameterError(chinese_msg='序列号不存在'))
            sequence = sequence.first()
            project = sequence.project
            user = project.user
            # 判断用户
            if user.username != request.user.username:
                return Response(ParameterError(chinese_msg='该序列号不属于当前用户'))
            # 判断是否更新图片
            informed_consent_file = sample_form.cleaned_data['informed_consent_file']
            if informed_consent_file:
                informed_consent = project.informed_consent
                remove_file(informed_consent.file_path)
                informed_consent_dir_path = os.path.join(settings.USER_IMAGES_DATA_DIR_PATH, 'informed_consent')
                informed_consent_file_path = os.path.join(informed_consent_dir_path, informed_consent_file.name)
                if handle_uploaded_file(informed_consent_file, informed_consent_file_path) and is_image_file(
                        informed_consent_file_path):
                    informed_consent.file_path = informed_consent_file_path
                    informed_consent.save()
                else:
                    remove_file(informed_consent_file_path)
                    return Response(ParameterError(chinese_msg='上传的不是图片文件'))
            project.remarks_json['contact_phone'] = sample_form.cleaned_data['contact_phone']
            project.remarks_json['wear_glasses_first_time'] = sample_form.cleaned_data['wear_glasses_first_time']
            project.remarks_json['family_history'] = sample_form.cleaned_data['family_history']
            project.remarks_json['optometry_left'] = sample_form.cleaned_data['optometry_left']
            project.remarks_json['optometry_right'] = sample_form.cleaned_data['optometry_right']
            self.set_user_info(user, sample_form.cleaned_data)
            return Response(Success(chinese_msg='更新成功'))
        else:
            return Response(ParameterError(msg_detail=str(sample_form.errors)))
