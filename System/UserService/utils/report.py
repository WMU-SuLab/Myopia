# -*- encoding: utf-8 -*-
"""
@File Name      :   report.py    
@Create Time    :   2022/4/8 19:19
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

from Common.models.project import Project
from Common.utils.http.exceptions import NotFound
    

def student_pdf_file_name(name: str) -> str:
    return 'student-'+name+'-report.pdf'


def teacher_pdf_file_name(name: str) -> str:
    return 'teacher-' + name + '-report.pdf'

def handle_eyes(eye_data: dict, key: str, issue: str, greater_than: float = None, less_than: float = None) -> str:
    if greater_than and less_than:
        key_right = greater_than < eye_data[key + '_right'] <= less_than
        key_left = greater_than < eye_data[key + '_left'] <= less_than
    elif greater_than:
        key_right = eye_data[key + '_right'] >= greater_than
        key_left = eye_data[key + '_left'] >= greater_than
    elif less_than:
        key_right = eye_data[key + '_right'] <= less_than
        key_left = eye_data[key + '_left'] <= less_than
    else:
        return ''

    if key_right or key_left:
        if key_right and key_left:
            return '双眼' + issue
        elif key_right:
            return '右眼' + issue
        else:
            return '左眼' + issue
    else:
        return ''


def generate_report_suggestions(eye_data: dict) -> list:
    """
    生成报告建议
    """
    suggestions = [
        # 近视
        handle_eyes(eye_data, 'spherical_equivalent', '低度近视', -3.0, -0.5),
        handle_eyes(eye_data, 'spherical_equivalent', '中度近视', - 6.0, -3.0),
        handle_eyes(eye_data, 'spherical_equivalent', '高度近视', - 10.0, -6.0),
        handle_eyes(eye_data, 'spherical_equivalent', '重度近视', less_than=-10.0),
        # 远视
        handle_eyes(eye_data, 'spherical_equivalent', '低度远视', 0.75, 3.0),
        handle_eyes(eye_data, 'spherical_equivalent', '中度远视',  3.0, 5.0),
        handle_eyes(eye_data, 'spherical_equivalent', '高度远视', greater_than=5.0),
        # 矫正视力异常
        handle_eyes(eye_data, 'corrected_visual_acuity', '矫正视力轻微异常，请及时矫正',4.8 ,4.9),
        # 散光
        handle_eyes(eye_data, 'column', '轻中度散光', -3.0 ,-0.75, ),
        # 弱视
        handle_eyes(eye_data, 'column', '高度散光，有弱视可能', less_than=-3.0),
        handle_eyes(eye_data, 'corrected_visual_acuity', '矫正视力异常幅度较大，有弱视可能', less_than=4.8),
        # 眼压
        handle_eyes(eye_data, 'intraocular_tension', '眼压过低', less_than=10.0),
        # 眼轴
        handle_eyes(eye_data, 'intraocular_tension', '眼压过高', greater_than=21.0),
        handle_eyes(eye_data, 'axial_length', '眼轴过长', greater_than=26.5)
    ]
    if abs(eye_data['corrected_visual_acuity_right'] - eye_data['corrected_visual_acuity_left'])>=0.2:
        suggestions.append('双眼矫正视力相差过大，有弱视可能')
    suggestions = [suggestion for suggestion in suggestions if suggestion]
    # 正常
    if len(suggestions) == 0:
        suggestions.append('双眼全部正常，请继续保持，注意日常生活健康用眼')
    else:
        suggestions.append('斜视弱视问题建议去医院斜视弱视专科检查，其他问题建议进一步去医院视光学专科检查')
    return suggestions


def generate_report_data_from_project(project) -> dict:
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
    return {
        'name': project.user.name,
        'identification_card_number': project.user.identification_card_number,
        'student_number': project.user.student_role.student_number,
        'classname': project.user.student_role.classname,
        'sex': project.user.sex,
        **eye_data,
        'suggestions': suggestions
    }


def generate_student_report_data(name, identification_card_number, student_number):
    project = Project.objects.filter(user__name=name)
    if project.exists():
        project = project.filter(
            user__identification_card_number=identification_card_number,
            user__student_role__student_number=student_number
        ).prefetch_related('user', 'user__student_role', 'visual_chart', 'tono_meter', 'bio_meter',
                           'refractometer', ).first()
        if project:
            return generate_report_data_from_project(project)
        else:
            raise NotFound(
                msg='error identification_card_number or student_number',
                chinese_msg='身份证号或学号错误'
            )
    else:
        raise NotFound(msg='no this student',chinese_msg='没有找到该学生')


def generate_teacher_report_data(name, identification_card_number,teacher_number):
    project= Project.objects.filter(user__name=name)
    if project.exists():
        project = project.filter(
            user__identification_card_number=identification_card_number,
            user__teacher_role__teacher_number=teacher_number
        ).prefetch_related('user', 'user__teacher_role', 'visual_chart', 'tono_meter', 'bio_meter',
                           'refractometer', ).first()
        if project:
            return generate_report_data_from_project(project)
        else:
            raise NotFound(
                msg='error identification_card_number or student_number',
                chinese_msg='身份证号或教工号错误'
            )
    else:
        raise NotFound(msg='no this student', chinese_msg='没有找到该教师')