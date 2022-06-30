# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@ Time    :   2022/4/9 19:51
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

from django.shortcuts import reverse, redirect
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from Common.models.equipments import *
from Common.serializers.base.equipments import VisualChartBaseSerializer, BioMeterBaseSerializer, \
    OptometryBaseSerializer, \
    TonoMeterBaseSerializer, EyeGroundBaseSerializer, SequenceBaseSerializer, InformedConsentBaseSerializer, \
    QuestionnaireBaseSerializer
from Common.utils.auth.views.api import EmployeeIsAuthenticatedGenericAPIView
from Common.utils.http.exceptions import ParameterError, NotFound, MethodNotAllowed, InsufficientPreconditions
from Common.utils.http.successes import Success
from Common.utils.text_handler.hash import encrypt_text
from Common.viewModels.base import retrieve_model
from Common.viewModels.equipments.informed_consent import handle_upload_informed_consent
from Common.viewModels.equipments.sequence import handle_upload_sequence


class EquipmentGenericAPIView(EmployeeIsAuthenticatedGenericAPIView):
    equipment_model_name = None

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.project_id = None
        self.project = None

    def get_project(self, data):
        project_id = data.get('project_id', None)
        if not project_id:
            raise ParameterError(chinese_msg='项目id不能为空')
        project = retrieve_model(Project, model_id=project_id)
        self.project_id = project_id
        self.project = project
        return project

    def precondition(self, data):
        project = self.get_project(data)
        if self.equipment_model_name != 'informed_consent' and getattr(project, 'has_informed_consent', False):
            raise InsufficientPreconditions(chinese_msg='还未填写知情同意书')
        if self.equipment_model_name != 'questionnaire' and getattr(project, 'has_questionnaire', False):
            raise InsufficientPreconditions(chinese_msg='还未填写问卷')
        if self.equipment_model_name != 'visual_chart' and getattr(project, 'has_visual_chart', False):
            raise InsufficientPreconditions(chinese_msg='还未做视力表')

    def set_equipment_pk(self, data):
        project = self.get_project(data)
        if not getattr(project, 'has_' + self.equipment_model_name, False):
            raise NotFound(chinese_msg='无相关数据')
        self.kwargs['pk'] = getattr(project, self.equipment_model_name).id


class EquipmentCreateRetrieveUpdateGenericAPIView(EquipmentGenericAPIView, RetrieveUpdateAPIView, CreateAPIView):
    def post(self, request, *args, **kwargs):
        self.precondition(request.data)
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.set_equipment_pk(request.data)
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.set_equipment_pk(request.data)
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return Response(MethodNotAllowed(chinese_msg='不支持该方法'))
        # if self.set_equipment_pk(request.data):
        #     return super().put(request, *args, **kwargs)
        # return Response(NotFound(chinese_msg='无数据'))


class InformedConsentCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = InformedConsent.objects.all()
    serializer_class = InformedConsentBaseSerializer
    equipment_model_name = 'informed_consent'

    def get(self, request, *args, **kwargs):
        self.set_equipment_pk(request.data)
        pk = self.kwargs['pk']
        informed_consent = retrieve_model(InformedConsent, model_id=pk)
        encrypted_file_text = encrypt_text(informed_consent.file_path)
        return redirect(
            reverse('Common:views:api:download_file', kwargs={'encrypted_file_text': encrypted_file_text}))

    def post(self, request, *args, **kwargs):
        return handle_upload_informed_consent(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return handle_upload_informed_consent(request, *args, **kwargs)


class QuestionnaireCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireBaseSerializer
    equipment_model_name = 'questionnaire'


class VisualChartCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = VisualChart.objects.all()
    serializer_class = VisualChartBaseSerializer
    equipment_model_name = 'visual_chart'


class BioMeterCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = BioMeter.objects.all()
    serializer_class = BioMeterBaseSerializer
    equipment_model_name = 'bio_meter'


class OptometryCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = Optometry.objects.all()
    serializer_class = OptometryBaseSerializer
    equipment_model_name = 'optometry'


class TonoMeterCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = TonoMeter.objects.all()
    serializer_class = TonoMeterBaseSerializer
    equipment_model_name = 'tono_meter'


class EyeGroundCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = EyeGround.objects.all()
    serializer_class = EyeGroundBaseSerializer
    equipment_model_name = 'eye_ground'


class SequenceCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = Sequence.objects.all()
    serializer_class = SequenceBaseSerializer
    equipment_model_name = 'sequence'

    def get(self, request, *args, **kwargs):
        self.set_equipment_pk(request.data)
        pk = self.kwargs['pk']
        sequence = retrieve_model(Sequence, model_id=pk)
        return Response(Success(data=sequence.serial_number, chinese_msg='创建成功'))

    def post(self, request, *args, **kwargs):
        self.precondition(request.data)
        return handle_upload_sequence(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return handle_upload_sequence(request, *args, **kwargs)
