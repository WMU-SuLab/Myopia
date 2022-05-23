# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@Create Time    :   2022/5/23 10:46
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

from Common.models.equipments import *
from Common.utils.auth.permissions import ModelViewPermission, ModelAddPermission, ModelChangePermission, \
    ModelDeletePermission


class CanViewVisualChart(ModelViewPermission):
    model = VisualChart


class CanAddVisualChart(ModelAddPermission):
    model = VisualChart


class CanChangeVisualChart(ModelChangePermission):
    model = VisualChart


class CanDeleteVisualChart(ModelDeletePermission):
    model = VisualChart


class CanViewBioMeter(ModelViewPermission):
    model = BioMeter


class CanAddBioMeter(ModelAddPermission):
    model = BioMeter


class CanChangeBioMeter(ModelChangePermission):
    model = BioMeter


class CanDeleteBioMeter(ModelDeletePermission):
    model = BioMeter


class CanViewOptometry(ModelViewPermission):
    model = Optometry


class CanAddOptometry(ModelAddPermission):
    model = Optometry


class CanChangeOptometry(ModelChangePermission):
    model = Optometry


class CanDeleteOptometry(ModelDeletePermission):
    model = Optometry


class CanViewTonoMeter(ModelViewPermission):
    model = TonoMeter


class CanAddTonoMeter(ModelAddPermission):
    model = TonoMeter


class CanChangeTonoMeter(ModelChangePermission):
    model = TonoMeter


class CanDeleteTonoMeter(ModelDeletePermission):
    model = TonoMeter


class CanViewEyeGround(ModelViewPermission):
    model = EyeGround


class CanAddEyeGround(ModelAddPermission):
    model = EyeGround


class CanChangeEyeGround(ModelChangePermission):
    model = EyeGround


class CanDeleteEyeGround(ModelDeletePermission):
    model = EyeGround


class CanViewSequence(ModelViewPermission):
    model = Sequence


class CanAddSequence(ModelAddPermission):
    model = Sequence


class CanChangeSequence(ModelChangePermission):
    model = Sequence


class CanDeleteSequence(ModelDeletePermission):
    model = Sequence


class CanViewInformedConsent(ModelViewPermission):
    model = InformedConsent


class CanAddInformedConsent(ModelAddPermission):
    model = InformedConsent


class CanChangeInformedConsent(ModelChangePermission):
    model = InformedConsent


class CanDeleteInformedConsent(ModelDeletePermission):
    model = InformedConsent


class CanViewQuestionnaire(ModelViewPermission):
    model = Questionnaire


class CanAddQuestionnaire(ModelAddPermission):
    model = Questionnaire


class CanChangeQuestionnaire(ModelChangePermission):
    model = Questionnaire


class CanDeleteQuestionnaire(ModelDeletePermission):
    model = Questionnaire
