# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@ Time    :   2022/4/8 18:44
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

from .equipments import VisualChartCreateRetrieveUpdateGenericAPIView, BioMeterCreateRetrieveUpdateGenericAPIView, \
    OptometryCreateRetrieveUpdateGenericAPIView, TonoMeterCreateRetrieveUpdateGenericAPIView, \
    EyeGroundCreateRetrieveUpdateGenericAPIView, SequenceCreateRetrieveUpdateGenericAPIView, \
    InformedConsentCreateRetrieveUpdateGenericAPIView, QuestionnaireCreateRetrieveUpdateGenericAPIView
from .project import ProjectRetrieveAPIView
from .user import UserPermissionsAPIView

urlpatterns = [
    # employee user
    path('employee/permissions', UserPermissionsAPIView.as_view(), name='employee_permissions'),
    # project
    path('projects/<int:project_id>', ProjectRetrieveAPIView.as_view(), name='get_project'),
    # equipments
    path('equipments/informed_consent', InformedConsentCreateRetrieveUpdateGenericAPIView.as_view(),
         name='equipments_informed_consent'),
    path('equipments/questionnaire', QuestionnaireCreateRetrieveUpdateGenericAPIView.as_view(),
         name='equipments_questionnaire'),
    path('equipments/visual_chart', VisualChartCreateRetrieveUpdateGenericAPIView.as_view(),
         name='equipments_visual_chart'),
    path('equipments/bio_meter', BioMeterCreateRetrieveUpdateGenericAPIView.as_view(), name='equipments_bio_meter'),
    path('equipments/optometry', OptometryCreateRetrieveUpdateGenericAPIView.as_view(), name='equipments_optometry'),
    path('equipments/tono_meter', TonoMeterCreateRetrieveUpdateGenericAPIView.as_view(), name='equipments_tono_meter'),
    path('equipments/eye_ground', EyeGroundCreateRetrieveUpdateGenericAPIView.as_view(), name='equipments_eye_ground'),
    path('equipments/sequence', SequenceCreateRetrieveUpdateGenericAPIView.as_view(), name='equipments_sequence'),

]
