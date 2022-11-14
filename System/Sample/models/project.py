# -*- encoding: utf-8 -*-
"""
@File Name      :   projects.py
@Create Time    :   2022/11/12 17:48
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


class HighMyopiaSampleProject(Project):
    progress_choices = (
        (-1, '未知'),
        (0, '初始化'),
        (1, '已登记'),
        (2, '收样中'),
        (3, '已收样'),
        (4, '分析中'),
        (5, '出报告'),
        (6, '已完成'),
    )

    def __init__(self, *args, **kwargs):
        super(HighMyopiaSampleProject, self).__init__(*args, **kwargs)
        self._meta.get_field('progress').choices = self.progress_choices

    class Meta:
        proxy = True


class TGFBISampleProject(Project):
    progress_choices = (
        (-1, '未知'),
        (0, '初始化'),
        (1, '样本绑定'),
        (2, '样本寄出'),
        (3, '已收样'),
        (4, '分析中'),
        (5, '出报告'),
        (6, '已完成'),
    )

    def __init__(self, *args, **kwargs):
        super(TGFBISampleProject, self).__init__(*args, **kwargs)
        self._meta.get_field('progress').choices = self.progress_choices

    class Meta:
        proxy = True
