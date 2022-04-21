# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/4/11 20:20
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

from pydantic import BaseModel

from Common.models.equipments import *
from Common.utils.text_handler.dicts import parameters_to_dict
from Common.utils.text_handler.identity_card import get_age
from Common.viewModels.equipments import count_spherical_equivalent


def update_or_create_project_data(project: Project, row):
    # 视力表
    uncorrected_visual_acuity_left = row['左裸眼视力']
    uncorrected_visual_acuity_right = row['右裸眼视力']
    corrected_visual_acuity_right = row['右矫正视力']
    corrected_visual_acuity_left = row['左矫正视力']
    glasses_type = row['眼镜类型']
    if uncorrected_visual_acuity_left and uncorrected_visual_acuity_right and glasses_type == '无':
        VisualChart.objects.update_or_create(
            project=project,
            defaults=parameters_to_dict(
                distance=5,
                uncorrected_visual_acuity_right=uncorrected_visual_acuity_right,
                uncorrected_visual_acuity_left=uncorrected_visual_acuity_left,
                glasses_type='none',
                remarks=row['备注']
            )
        )
    else:
        VisualChart.objects.update_or_create(
            project=project,
            defaults=parameters_to_dict(
                distance=5,
                corrected_visual_acuity_right=corrected_visual_acuity_right,
                corrected_visual_acuity_left=corrected_visual_acuity_left,
                glasses_type=glasses_type,
                remarks=row['备注']
            )
        )
    # 生物测量仪
    BioMeter.objects.update_or_create(
        project=project,
        defaults=parameters_to_dict(
            axial_length_right=row['右眼眼轴长度(AL)'],
            axial_length_left=row['左眼眼轴长度(AL)'],

            corneal_thickness_right=row['右眼角膜厚度(CCT)'],
            corneal_thickness_left=row['左眼角膜厚度(CCT)'],

            chamber_depth_right=row['右眼前房深度(AD)'],
            chamber_depth_left=row['左眼前房深度(AD)'],

            corneal_curvature_right_K1=row['右眼角膜曲率(K1)'],
            corneal_curvature_left_K1=row['左眼角膜曲率(K1)'],
            corneal_curvature_right_K2=row['右眼角膜曲率(K2)'],
            corneal_curvature_left_K2=row['左眼角膜曲率(K2)'],
            corneal_curvature_right_AST=row['右眼角膜曲率(AST)'],
            corneal_curvature_left_AST=row['左眼角膜曲率(AST)'],
            corneal_curvature_right_n=row['右眼角膜曲率(n)'],
            corneal_curvature_left_n=row['左眼角膜曲率(n)'],

            white_to_white_right=row['右眼白到白距离(WTW)'],
            white_to_white_left=row['左眼白到白距离(WTW)'],

            lens_thickness_right=row['右眼晶状体厚度(LT)'],
            lens_thickness_left=row['左眼晶状体厚度(LT)'],

            pupil_diameter_right=row['右眼瞳孔直径(PD)'],
            pupil_diameter_left=row['左眼瞳孔直径(PD)'],

            ACD_right=row['右眼ACD'],
            ACD_left=row['左眼ACD'],
        )
    )
    Refractometer.objects.update_or_create(
        project=project,
        defaults=parameters_to_dict(
            spherical_right=row['右球镜s'],
            spherical_left=row['左球镜s'],

            column_right=row['右柱镜c'],
            column_left=row['左柱镜c'],

            SE_right=count_spherical_equivalent(row['右球镜s'], row['右柱镜c']),
            SE_left=count_spherical_equivalent(row['左球镜s'], row['左柱镜c']),

            axis_right=row['右轴位a'],
            axis_left=row['左轴位a'],

            interpupillary_distance=row['瞳距pd'],
        )
    )
    TonoMeter.objects.update_or_create(
        project=project,
        defaults=parameters_to_dict(
            intraocular_tension_right=row['右眼眼压'],
            intraocular_tension_left=row['左眼眼压']
        )
    )
    Sequence.objects.update_or_create(
        project=project,
        defaults=parameters_to_dict(
            serial_number=row['条形码']
        )
    )


def export_project_data(project:Project.objects.filter()):
    # todo
    pass

class Suggestion(BaseModel):
    eye: str = None
    key: str = None
    issue: str = None
    level: int = None
    classification: int = None


def handle_eyes(eye_data: dict, key: str, issue: str, level: int, classification: int, greater_than: float = None,
                less_than: float = None,
                ) -> dict:
    """
    处理眼睛数据
    :param eye_data:
    :param key: 有问题的字段
    :param issue:
    :param classification: 分级
    :param level: 等级
    :param greater_than:
    :param less_than:
    :return:
    """
    if not eye_data:
        return {}
    eye_data_right = eye_data[key + '_right']
    eye_data_left = eye_data[key + '_left']
    if greater_than and less_than:
        key_right = greater_than < eye_data_right <= less_than if eye_data_right else False
        key_left = greater_than < eye_data_left <= less_than if eye_data_left else False
    elif greater_than:
        key_right = eye_data_right >= greater_than if eye_data_right else False
        key_left = eye_data_left >= greater_than if eye_data_left else False
    elif less_than:
        key_right = eye_data_right <= less_than if eye_data_right else False
        key_left = eye_data_left <= less_than if eye_data_left else False
    else:
        return {}

    suggestion = Suggestion(
        **{
            'eye': '',
            'key': key,
            'issue': '',
            'level': level,
            'classification': classification,
        }
    )
    if key_right or key_left:
        if key_right and key_left:
            suggestion.eye = 'all'
            suggestion.issue = '双眼' + issue
        elif key_right:
            suggestion.eye = 'right'
            suggestion.issue = '右眼' + issue
        else:
            suggestion.eye = 'left'
            suggestion.issue = '左眼' + issue
        return suggestion.dict()
    else:
        return {}


def generate_report_suggestions(eye_data: dict) -> list:
    """
    生成报告建议
    """
    suggestions = [
        # 近视
        handle_eyes(eye_data, 'spherical_equivalent', '低度近视', 1, 4, -3.0, -0.5),
        handle_eyes(eye_data, 'spherical_equivalent', '中度近视', 2, 4, - 6.0, -3.0),
        handle_eyes(eye_data, 'spherical_equivalent', '高度近视', 3, 4, - 10.0, -6.0),
        handle_eyes(eye_data, 'spherical_equivalent', '重度近视', 4, 4, less_than=-10.0),
        # 远视
        handle_eyes(eye_data, 'spherical_equivalent', '低度远视', 1, 3, 0.75, 3.0),
        handle_eyes(eye_data, 'spherical_equivalent', '中度远视', 2, 3, 3.0, 5.0),
        handle_eyes(eye_data, 'spherical_equivalent', '高度远视', 3, 3, greater_than=5.0),
        # 矫正视力异常
        handle_eyes(eye_data, 'corrected_visual_acuity', '矫正视力轻微异常，请及时矫正', 1, 1, 4.8, 4.9),
        # 散光
        handle_eyes(eye_data, 'column', '轻中度散光', 1, 2, -3.0, -0.75, ),
        # 弱视
        handle_eyes(eye_data, 'column', '高度散光，有弱视可能', 2, 2, less_than=-3.0),
        handle_eyes(eye_data, 'corrected_visual_acuity', '矫正视力异常幅度较大，有弱视可能', 1, 1, less_than=4.8),
        # 眼压
        handle_eyes(eye_data, 'intraocular_tension', '眼压过低', 1, 1, less_than=10.0),
        # 眼轴
        handle_eyes(eye_data, 'intraocular_tension', '眼压过高', 1, 1, greater_than=21.0),
        handle_eyes(eye_data, 'axial_length', '眼轴过长', 1, 1, greater_than=26.5)
    ]
    if eye_data['corrected_visual_acuity_right'] and eye_data['corrected_visual_acuity_left']:
        if abs(eye_data['corrected_visual_acuity_right'] - eye_data['corrected_visual_acuity_left']) >= 0.2:
            suggestions.append(Suggestion(issue='双眼矫正视力相差过大，有弱视可能').dict())
    suggestions = [suggestion for suggestion in suggestions if suggestion]
    # 正常
    if len(suggestions) == 0:
        suggestions.append(Suggestion(issue='双眼全部正常，请继续保持，注意日常生活健康用眼').dict())
    else:
        suggestions.append(Suggestion(issue='斜视弱视问题建议去医院斜视弱视专科检查，其他问题建议进一步去医院视光学专科检查').dict())
    return suggestions


def generate_report_data_from_project(project) -> dict:
    report_data = project.remarks_json.get('report_data', None)
    if report_data:
        return report_data
    uncorrected_visual_acuity_right = project.visual_chart.uncorrected_visual_acuity_right
    uncorrected_visual_acuity_left = project.visual_chart.uncorrected_visual_acuity_left
    corrected_visual_acuity_right = project.visual_chart.corrected_visual_acuity_right
    corrected_visual_acuity_left = project.visual_chart.corrected_visual_acuity_left
    if corrected_visual_acuity_right and corrected_visual_acuity_left:
        corrected_visual_acuity_right = uncorrected_visual_acuity_right
        corrected_visual_acuity_left = uncorrected_visual_acuity_left

    eye_data = {
        'corrected_visual_acuity_right': corrected_visual_acuity_right,
        'corrected_visual_acuity_left': corrected_visual_acuity_left,

        'intraocular_tension_right': project.tono_meter.intraocular_tension_right,
        'intraocular_tension_left': project.tono_meter.intraocular_tension_left,

        'axial_length_right': project.bio_meter.axial_length_right,
        'axial_length_left': project.bio_meter.axial_length_left,
        'corneal_thickness_right': project.bio_meter.corneal_thickness_right,
        'corneal_thickness_left': project.bio_meter.corneal_thickness_left,

        'spherical_right': project.refractometer.spherical_right,
        'spherical_left': project.refractometer.spherical_left,
        'column_right': project.refractometer.column_right,
        'column_left': project.refractometer.column_left,
        'axis_right': project.refractometer.axis_right,
        'axis_left': project.refractometer.axis_left,
        'spherical_equivalent_right': project.refractometer.spherical_right,
        'spherical_equivalent_left': project.refractometer.spherical_left,
    }
    suggestions = generate_report_suggestions(eye_data)
    report_data = {
        'name': project.user.name,
        'identification_card_number': project.user.identification_card_number,
        'student_number': project.user.student_role.student_number,
        'classname': project.user.student_role.classname,
        'sex': project.user.gender,
        'gender':project.user.get_gender_display(),
        'age': get_age(project.user.identification_card_number),
        **eye_data,
        'suggestions': suggestions
    }
    project.remarks_json['report_data'] = report_data
    project.save()
    return report_data
