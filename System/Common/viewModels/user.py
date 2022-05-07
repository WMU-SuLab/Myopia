# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/20 21:56
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

from Common.models.user import User

from .project import export_project_data


def export_users_projects_data(users: list[User]):
    return [export_project_data(project) for user in users for project in user.projects.select_related(
        'visual_chart', 'bio_meter', 'tono_meter', 'optometry', 'eye_ground', 'informed_consent', 'questionnaire',
        'sequence',
    ) if project.is_finished]
