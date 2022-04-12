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

from Common.models.equipments import *


def add_project_data(project: Project, row):
    # 视力表
    uncorrected_visual_acuity_left = row['左裸眼视力']
    uncorrected_visual_acuity_right = row['右裸眼视力']
    corrected_visual_acuity_right = row['右矫正视力']
    corrected_visual_acuity_left = row['左矫正视力']
    glasses_type = row['眼镜类型']
    if uncorrected_visual_acuity_left and uncorrected_visual_acuity_right and glasses_type == '无':
        VisualChart.objects.create(
            project=project,
            distance=5,
            uncorrected_visual_acuity_right=uncorrected_visual_acuity_right,
            uncorrected_visual_acuity_left=uncorrected_visual_acuity_left,
            glasses_type='裸眼',
            remarks=row['备注']
        )
    else:
        VisualChart.objects.create(
            project=project,
            distance=5,
            corrected_visual_acuity_right=corrected_visual_acuity_right,
            corrected_visual_acuity_left=corrected_visual_acuity_left,
            glasses_type=glasses_type,
            remarks=row['备注']
        )
    # 生物测量仪
    BioMeter.objects.create(
        project=project,
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
    Refractometer.objects.create(
        project=project,
        spherical_right=row['右球镜s'],
        spherical_left=row['左球镜s'],

        column_right=row['右柱镜c'],
        column_left=row['左柱镜c'],

        SE_right=row['右眼SE'],
        SE_left=row['左眼SE'],

        axis_right=row['右轴位a'],
        axis_left=row['左轴位a'],

        interpupillary_distance=row['瞳距pd'],
    )
    TonoMeter.objects.create(
        project=project,
        intraocular_tension_right=row['右眼眼压'],
        intraocular_tension_left=row['左眼眼压']
    )
    Sequence.objects.create(
        project=project,
        serial_number=row['条形码']
    )
