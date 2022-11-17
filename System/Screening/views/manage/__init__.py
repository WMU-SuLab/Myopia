# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/4/8 19:01
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

from django.urls import path

from .equipments import *
from .index import index, home, statistics
from .project import project, project_wmu
from .tools import myopia_risk_prediction
from .user import login, user

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('statistics/', statistics, name='statistics'),
    path('user/', user, name='user'),
    path('project/', project, name='project'),
    path('project/wmu', project_wmu, name='project_wmu'),
    path('equipments/visual_chart', visual_chart, name='equipments_visual_chart'),
    path('equipments/bio_meter', bio_meter, name='equipments_bio_meter'),
    path('equipments/optometry', optometry, name='equipments_optometry'),
    path('equipments/tono_meter', tono_meter, name='equipments_tono_meter'),
    path('equipments/eye_ground', eye_ground, name='equipments_eye_ground'),
    path('equipments/sequence', sequence, name='equipments_sequence'),
    path('equipments/informed_consent', informed_consent, name='equipments_informed_consent'),
    path('equipments/questionnaire', questionnaire, name='equipments_questionnaire'),
    path('tools/myopia_risk_prediction', myopia_risk_prediction, name='tools_myopia_risk_prediction'),
]
