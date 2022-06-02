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

from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from Common.models.equipments import *
from Common.serializers.base.equipments import VisualChartBaseSerializer, BioMeterBaseSerializer, \
    OptometryBaseSerializer, \
    TonoMeterBaseSerializer, EyeGroundBaseSerializer, SequenceBaseSerializer, InformedConsentBaseSerializer, \
    QuestionnaireBaseSerializer
from Common.utils.http.exceptions import ParameterError, NotFound, PreconditionFailed
from Common.viewModels.base import retrieve_model
from Screening.utils.auth.views.api import EmployeeIsAuthenticatedGenericAPIView


class EquipmentGenericAPIView(EmployeeIsAuthenticatedGenericAPIView):
    equipment_model_name = None

    def get_project(self, data):
        project_id = data.get('project_id', None)
        if not project_id:
            raise ParameterError(chinese_msg='项目id不能为空')
        return retrieve_model(Project, model_id=project_id)

    def precondition(self, data):
        project = self.get_project(data)
        if self.equipment_model_name != 'visual_chart' and getattr(project, 'has_visual_chart', False):
            raise PreconditionFailed(chinese_msg='还未做视力表')
        return True

    def set_equipment_pk(self, data):
        project = self.get_project(data)
        if getattr(project, 'has_' + self.equipment_model_name, False):
            self.kwargs['pk'] = getattr(project, self.equipment_model_name).id
            return True
        return False


class EquipmentCreateRetrieveUpdateGenericAPIView(EquipmentGenericAPIView, RetrieveUpdateAPIView, CreateAPIView):
    def post(self, request, *args, **kwargs):
        if self.precondition(request.data):
            return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.set_equipment_pk(request.data):
            return super().get(request, *args, **kwargs)
        return Response(NotFound(chinese_msg='无数据'))

    def put(self, request, *args, **kwargs):
        if self.set_equipment_pk(request.data):
            return super().put(request, *args, **kwargs)
        return Response(NotFound(chinese_msg='无数据'))

    def patch(self, request, *args, **kwargs):
        if self.set_equipment_pk(request.data):
            return super().patch(request, *args, **kwargs)
        return Response(NotFound(chinese_msg='无数据'))


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


class InformedConsentCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = InformedConsent.objects.all()
    serializer_class = InformedConsentBaseSerializer
    equipment_model_name = 'informed_consent'


class QuestionnaireCreateRetrieveUpdateGenericAPIView(EquipmentCreateRetrieveUpdateGenericAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireBaseSerializer
    equipment_model_name = 'questionnaire'
