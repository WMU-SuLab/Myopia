# -*- encoding: utf-8 -*-
"""
@File Name      :   choices.py
@Create Time    :   2022/11/13 17:54
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

gender_choices = (
    (0, '未知'),
    (1, '男'),
    (2, '女')
)
identification_card_type_choices = (
    (0, '其他'),
    (1, '居民身份证'),
    (2, '港澳居民来往内地通行证'),
    (3, '台湾居民来往大陆通行证'),
    (4, '护照'),
    (5, '军官证'),
    (6, '士兵证'),
    (7, '外国人居留证'),
)

education_choices = (
    (-1, '其他'),
    (0, '未受过教育'),
    (1, '幼儿园'),
    (2, '小学'),
    (3, '初级中学'),
    (4, '高级中学（中专）'),
    (5, '大学专科'),
    (6, '大学本科'),
    (7, '硕士研究生'),
    (8, '博士研究生'),
)

student_type_choices = (
    (-1, '未知'),
    (1, '学龄前儿童'),
    (2, '小学生'),
    (3, '初中生'),
    (4, '高中生'),
    (5, '大学生'),
    (6, '硕士研究生'),
    (7, '博士研究生'),
    (8, '博士后'),
)

common_progress_choices = (
    (-1, '未知'),
    (0, '初始化'),
    (1, '已完成'),
)
