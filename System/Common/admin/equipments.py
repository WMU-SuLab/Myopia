# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@Create Time    :   2022/4/29 16:57
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

from django.contrib import admin

from Common.models.equipments import *
from .base import BaseAdmin


@admin.register(VisualChart)
class VisualChartAdmin(BaseAdmin):
    pass


@admin.register(BioMeter)
class BioMeterAdmin(BaseAdmin):
    pass


@admin.register(Optometry)
class OptometryAdmin(BaseAdmin):
    pass


@admin.register(TonoMeter)
class TonoMeterAdmin(BaseAdmin):
    pass


@admin.register(EyeGround)
class EyeGroundAdmin(BaseAdmin):
    pass


@admin.register(Sequence)
class SequenceAdmin(BaseAdmin):
    pass


@admin.register(InformedConsent)
class InformedConsentAdmin(BaseAdmin):
    pass


@admin.register(Questionnaire)
class QuestionnaireAdmin(BaseAdmin):
    pass
