# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@Create Time    :   2022/5/11 13:41
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

from rest_framework import serializers

from Common.models.equipments import *
from . import base_exclude, BaseSerializer

equipments_exclude = base_exclude


class EquipmentsBaseSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        # fields = '__all__'
        exclude = equipments_exclude


class VisualChartBaseSerializer(EquipmentsBaseSerializer):
    glasses_type_display = serializers.CharField(source='get_glasses_type_display', required=False)

    class Meta(EquipmentsBaseSerializer.Meta):
        model = VisualChart
        extra_kwargs = {
            **EquipmentsBaseSerializer.Meta.extra_kwargs,
            'uncorrected_visual_acuity_right': {'required': False},
            'uncorrected_visual_acuity_left': {'required': False},
            'corrected_visual_acuity_right': {'required': False},
            'corrected_visual_acuity_left': {'required': False},
            'glasses_type': {'required': False},
        }


class BioMeterBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = BioMeter


class OptometryBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = Optometry


class TonoMeterBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = TonoMeter


class EyeGroundBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = EyeGround


class SequenceBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = Sequence


class InformedConsentBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = InformedConsent


class QuestionnaireBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = Questionnaire
