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


class VisualChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisualChart
        fields = '__all__'


class BioMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioMeter
        fields = '__all__'


class OptometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Optometry
        fields = '__all__'


class TonoMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TonoMeter
        fields = '__all__'


class EyeGroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeGround
        fields = '__all__'


class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'


class InformedConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformedConsent
        fields = '__all__'


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
