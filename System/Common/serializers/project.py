# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/5/5 15:25
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

from .base.equipments import VisualChartBaseSerializer, BioMeterBaseSerializer, OptometryBaseSerializer, \
    TonoMeterBaseSerializer, EyeGroundBaseSerializer, SequenceBaseSerializer, InformedConsentBaseSerializer, \
    QuestionnaireBaseSerializer
from .base.project import ProjectBaseSerializer
from .base.user import UserBaseSerializer


class ProjectUserSerializer(ProjectBaseSerializer):
    user = UserBaseSerializer()

    class Meta(ProjectBaseSerializer.Meta):
        depth = 1


class ProjectEquipmentsBaseSerializer(ProjectBaseSerializer):
    informed_consent = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    questionnaire = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    visual_chart = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    bio_meter = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    optometry = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    tono_meter = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    eye_ground = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    sequence = serializers.PrimaryKeyRelatedField(read_only=True, required=False)


class ProjectEquipmentsSerializer(ProjectBaseSerializer):
    informed_consent = InformedConsentBaseSerializer()
    questionnaire = QuestionnaireBaseSerializer()
    visual_chart = VisualChartBaseSerializer()
    bio_meter = BioMeterBaseSerializer()
    optometry = OptometryBaseSerializer()
    tono_meter = TonoMeterBaseSerializer()
    eye_ground = EyeGroundBaseSerializer()
    sequence = SequenceBaseSerializer()
