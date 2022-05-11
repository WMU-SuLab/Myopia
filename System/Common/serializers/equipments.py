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

from .base.equipments import *


class EquipmentsSerializerMeta(EquipmentsBaseSerializer.Meta):
    depth = 2


class VisualChartSerializer(VisualChartBaseSerializer):
    class Meta(EquipmentsSerializerMeta, VisualChartBaseSerializer.Meta):
        pass


class BioMeterSerializer(BioMeterBaseSerializer):
    class Meta(EquipmentsSerializerMeta, BioMeterBaseSerializer.Meta):
        pass


class OptometrySerializer(OptometryBaseSerializer):
    class Meta(EquipmentsSerializerMeta, OptometryBaseSerializer.Meta):
        pass


class TonoMeterSerializer(TonoMeterBaseSerializer):
    class Meta(EquipmentsSerializerMeta, TonoMeterBaseSerializer.Meta):
        pass


class EyeGroundSerializer(EyeGroundBaseSerializer):
    class Meta(EquipmentsSerializerMeta, EyeGroundBaseSerializer.Meta):
        pass


class SequenceSerializer(SequenceBaseSerializer):
    class Meta(EquipmentsSerializerMeta, SequenceBaseSerializer.Meta):
        pass


class InformedConsentSerializer(InformedConsentBaseSerializer):
    class Meta(EquipmentsSerializerMeta, InformedConsentBaseSerializer.Meta):
        pass


class QuestionnaireSerializer(QuestionnaireBaseSerializer):
    class Meta(EquipmentsSerializerMeta, QuestionnaireBaseSerializer.Meta):
        pass
