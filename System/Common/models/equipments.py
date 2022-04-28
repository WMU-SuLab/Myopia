# -*- encoding: utf-8 -*-
"""
@File Name      :   instrument.py    
@Create Time    :   2022/3/29 11:01
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

from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.db import models

from .base import Base
from .project import Project


class VisualChart(Base):
    """
    视力表
    """
    glasses = (
        ('none', '无(裸眼)'),
        ('normal', '框架眼镜'),
        ('contact_lenses', '隐形眼镜'),
        ('OK', '角膜塑形镜'),
    )

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='visual_chart', verbose_name='项目')

    distance = models.FloatField(max_length=2, validators=[MinValueValidator(0)], default=5,
                                 verbose_name='测量距离，单位：米(m)')

    eyesight_range_validators = [MinValueValidator(0), MaxValueValidator(5.3), DecimalValidator(2, 1)]
    uncorrected_visual_acuity_right = models.FloatField(validators=eyesight_range_validators, null=True, blank=True,
                                                        default=None, verbose_name='右眼未校正/裸眼视力')
    uncorrected_visual_acuity_left = models.FloatField(validators=eyesight_range_validators, null=True, blank=True,
                                                       default=None, verbose_name='左眼未校正/裸眼视力')

    corrected_visual_acuity_right = models.FloatField(validators=eyesight_range_validators, null=True, blank=True,
                                                      default=None, verbose_name='右眼校正/裸眼视力')
    corrected_visual_acuity_left = models.FloatField(validators=eyesight_range_validators, null=True, blank=True,
                                                     default=None, verbose_name='左眼校正/裸眼视力')

    glasses_type = models.CharField(max_length=50, choices=glasses, null=True, blank=True, default=None,
                                    verbose_name='眼镜类型')

    class Meta:
        verbose_name = verbose_name_plural = '视力表'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class BioMeter(Base):
    """
    生物测量仪
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='bio_meter', verbose_name='项目')

    axial_length_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼轴长(AL)')
    axial_length_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼轴长(AL)')

    corneal_thickness_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼角膜厚度(CCT)')
    corneal_thickness_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼角膜厚度(CCT)')

    chamber_depth_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼前房深度(AD)')
    chamber_depth_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼前房深度(AD)')

    corneal_curvature_right_K1 = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼角膜曲率(K1)')
    corneal_curvature_left_K1 = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼角膜曲率(K1)')
    corneal_curvature_right_K2 = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼角膜曲率(K2)')
    corneal_curvature_left_K2 = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼角膜曲率(K2)')
    corneal_curvature_right_AST = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼角膜曲率(AST)')
    corneal_curvature_left_AST = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼角膜曲率(AST)')
    corneal_curvature_right_n = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼角膜曲率(n)')
    corneal_curvature_left_n = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼角膜曲率(n)')

    white_to_white_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼白到白距离(WTW)')
    white_to_white_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼白到白距离(WTW)')

    lens_thickness_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼晶状体厚度(LT)')
    lens_thickness_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼晶状体厚度(LT)')

    pupil_diameter_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼瞳孔直径(PD)')
    pupil_diameter_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼瞳孔直径(PD)')

    ACD_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼ACD')
    ACD_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼ACD')

    class Meta:
        verbose_name = verbose_name_plural = '生物测量仪'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class Optometry(Base):
    """
    电脑验光仪
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='optometry', verbose_name='项目')

    spherical_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右球镜s')
    spherical_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左球镜s')

    column_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右柱镜c')
    column_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左柱镜c')

    SE_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右眼等效球镜SE')
    SE_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左眼等效球镜SE')

    axis_right = models.FloatField(null=True, blank=True, default=None, verbose_name='右轴位a')
    axis_left = models.FloatField(null=True, blank=True, default=None, verbose_name='左轴位a')

    interpupillary_distance = models.FloatField(null=True, blank=True, default=None, verbose_name='瞳距pd')

    class Meta:
        verbose_name = verbose_name_plural = '电脑验光仪'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class TonoMeter(Base):
    """
    眼压计
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='tono_meter', verbose_name='项目')

    tension_validators = [MinValueValidator(0), MaxValueValidator(50), DecimalValidator(3, 1)]

    intraocular_tension_right = models.FloatField(
        validators=tension_validators, null=True, blank=True, default=None, verbose_name='右眼眼压(mmHg)')
    intraocular_tension_left = models.FloatField(
        validators=tension_validators, null=True, blank=True, default=None, verbose_name='左眼眼压(mmHg)')

    class Meta:
        verbose_name = verbose_name_plural = '眼压计'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class EyeGround(Base):
    """
    眼底照
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='eye_ground', verbose_name='项目')
    image_path_right = models.FilePathField(max_length=255, null=True, blank=True, default=None, verbose_name='右眼眼底图路径')
    image_path_left = models.FilePathField(max_length=255, null=True, blank=True, default=None, verbose_name='左眼眼底图路径')
    image_url_right = models.URLField(max_length=512, null=True, blank=True, default=None, verbose_name='右眼眼底图远程URL')
    image_url_left = models.URLField(max_length=512, null=True, blank=True, default=None, verbose_name='左眼眼底图远程URL')

    @property
    def image_location(self):
        return {
            'image_path_right': self.image_path_right,
            'image_path_left': self.image_path_left,
            'image_url_right': self.image_url_right,
            'image_url_left': self.image_url_left,
        }

    class Meta:
        verbose_name = verbose_name_plural = '眼底照'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class Sequence(Base):
    """
    测序
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='sequence', verbose_name='项目')
    serial_number = models.CharField(max_length=32, null=True, blank=True, default=None, verbose_name='测序编号')
    file_path = models.FilePathField(null=True, blank=True, default=None, verbose_name='测序文件路径')
    file_url = models.URLField(max_length=512, null=True, blank=True, default=None, verbose_name='测序文件远程URL')

    @property
    def file_location(self):
        return {'file_path': self.file_path, 'file_url': self.file_url}

    class Meta:
        verbose_name = verbose_name_plural = '测序'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class InformedConsent(Base):
    """
    知情同意书
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='informed_consent',
                                   verbose_name='项目')
    file_path = models.FilePathField(null=True, blank=True, default=None, verbose_name='知情同意书文件路径')
    file_url = models.CharField(max_length=512, null=True, blank=True, default=None, verbose_name='知情同意书文件远程URL')

    @property
    def file_location(self):
        return {'file_path': self.file_path, 'file_url': self.file_url}

    class Meta:
        verbose_name = verbose_name_plural = '知情同意书'

    def __str__(self):
        return f'Belong to project {self.project_id}'


class Questionnaire(Base):
    """
    问卷
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='questionnaire', verbose_name='项目')
    content = models.JSONField(null=True, blank=True, default=list, verbose_name='问卷内容')

    class Meta:
        verbose_name = verbose_name_plural = '问卷'

    def __str__(self):
        return f'Belong to project {self.project_id}'
