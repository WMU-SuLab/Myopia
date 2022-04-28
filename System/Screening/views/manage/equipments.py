# -*- encoding: utf-8 -*-
"""
@File Name      :   equipments.py    
@Create Time    :   2022/4/14 9:52
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

from django.shortcuts import render

from .index import screening_manage_login_required


@screening_manage_login_required
def visual_chart(request):
    return render(request, 'Screening/manage/equipments/visual_chart.html')


@screening_manage_login_required
def bio_meter(request):
    return render(request, 'Screening/manage/equipments/bio_meter.html')


@screening_manage_login_required
def optometry(request):
    return render(request, 'Screening/manage/equipments/optometry.html')


@screening_manage_login_required
def tono_meter(request):
    return render(request, 'Screening/manage/equipments/tono_meter.html')


@screening_manage_login_required
def eye_ground(request):
    return render(request, 'Screening/manage/equipments/eye_ground.html')


@screening_manage_login_required
def sequence(request):
    return render(request, 'Screening/manage/equipments/sequence.html')


@screening_manage_login_required
def informed_consent(request):
    return render(request, 'Screening/manage/equipments/informed_consent.html')


@screening_manage_login_required
def questionnaire(request):
    return render(request, 'Screening/manage/equipments/questionnaire.html')
