# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@Create Time    :   2022/5/5 15:26
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
from .base import base_exclude

equipments_exclude = base_exclude


class EquipmentsBaseSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = '__all__'
        exclude = equipments_exclude


class EquipmentsSerializerMeta(EquipmentsBaseSerializer.Meta):
    depth = 2


class VisualChartBaseSerializer(EquipmentsBaseSerializer):
    glasses_type = serializers.CharField(source='get_glasses_type_display')

    class Meta(EquipmentsBaseSerializer.Meta):
        model = VisualChart


class VisualChartSerializer(VisualChartBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = VisualChart


class BioMeterBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = BioMeter


class BioMeterSerializer(BioMeterBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = BioMeter


class OptometryBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = Optometry


class OptometrySerializer(OptometryBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = Optometry


class TonoMeterBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = TonoMeter


class TonoMeterSerializer(TonoMeterBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = TonoMeter


class EyeGroundBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = EyeGround


class EyeGroundSerializer(EyeGroundBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = EyeGround


class SequenceBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = Sequence


class SequenceSerializer(SequenceBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = Sequence


class InformedConsentBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = InformedConsent


class InformedConsentSerializer(InformedConsentBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = InformedConsent


class QuestionnaireBaseSerializer(EquipmentsBaseSerializer):
    class Meta(EquipmentsBaseSerializer.Meta):
        model = Questionnaire


class QuestionnaireSerializer(QuestionnaireBaseSerializer):
    class Meta(EquipmentsSerializerMeta):
        model = Questionnaire
