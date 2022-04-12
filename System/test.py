# -*- encoding: utf-8 -*-
"""
@File Name      :   test.py    
@Create Time    :   2022/4/4 16:28
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
# from collections import defaultdict
# import pandas as pd
# from jinja2 import Environment, FileSystemLoader
# # 测试完成后请删除所有代码
# from weasyprint import HTML
#
# suggestions_classify={
#     'normal':'视力测量未见明显异常',
#     'abnormal':'建议尽快到正规医院进一步就诊',
#     'myopia':'眼验光数据异常，建议每半年复查视力和屈光度数，做好爱眼护眼卫生',
#     'high_myopia':'眼验光数据异常',
#     'intraocular_tension_abnormal':'眼压异常',
#     'axial_length':'眼轴异常',
# }
#
# template_loader = FileSystemLoader('./Myopia/templates')
# template_env = Environment(loader=template_loader)
# template = template_env.get_template('Myopia/report/report.html')  # 获取一个模板文件
#
# abnormal_df = pd.read_excel('./20220301-20220323结果汇总-SHJ.xlsx', sheet_name='Sheet2')
# abnormal_students_id=[]
# abnormal_students= defaultdict(list)
# for index,row in abnormal_df.iterrows():
#     abnormal_students_id.append(row['学籍号'])
#     abnormal_students[row['学籍号']].append(row['表型'])
# abnormal_students_id=list(set(abnormal_students_id))
#
# student_df = pd.read_excel('./20220301-20220323结果汇总-SHJ.xlsx', sheet_name='Sheet1')
# students=[]
# for index, row in student_df.iterrows():
#     if row['学籍号'] in abnormal_students_id:
#         phenotype= ','.join(abnormal_students[row['学籍号']])
#         name = row['学生名称']
#         uncorrected_visual_acuity_left = row['左裸眼视力']
#         uncorrected_visual_acuity_right = row['右裸眼视力']
#         corrected_visual_acuity_left = row['左矫正视力']
#         corrected_visual_acuity_right = row['右矫正视力']
#         # print(corrected_visual_acuity_left)
#         # print(corrected_visual_acuity_right)
#         if pd.isnull(corrected_visual_acuity_left) and pd.isnull(corrected_visual_acuity_right):
#             corrected_visual_acuity_left = uncorrected_visual_acuity_left
#             corrected_visual_acuity_right = uncorrected_visual_acuity_right
#             # print(corrected_visual_acuity_left)
#             # print(corrected_visual_acuity_right)
#         intraocular_tension_left = row['左眼眼压']
#         intraocular_tension_right = row['右眼眼压']
#         axial_length_left = row['左眼眼轴长度(AL)']
#         axial_length_right = row['右眼眼轴长度(AL)']
#         corneal_thickness_left = row['左眼角膜厚度(CCT)']
#         corneal_thickness_right = row['右眼角膜厚度(CCT)']
#         spherical_left = row['左球镜s']
#         spherical_right = row['右球镜s']
#         column_left = row['左柱镜c']
#         column_right = row['右柱镜c']
#         axis_left = row['左轴位a']
#         axis_right = row['右轴位a']
#         spherical_equivalent_left = row['左眼SE']
#         spherical_equivalent_right = row['右眼SE']
#         suggestion=[]
#
#
#         student = {
#             'phenotype': phenotype,
#             'name': name,
#             'gender': '男',
#             'age': 20,
#             'corrected_visual_acuity_left': corrected_visual_acuity_left,
#             'corrected_visual_acuity_right': corrected_visual_acuity_right,
#             'intraocular_tension_left': intraocular_tension_left,
#             'intraocular_tension_right': intraocular_tension_right,
#             'axial_length_left': axial_length_left,
#             'axial_length_right': axial_length_right,
#             'corneal_thickness_left': corneal_thickness_left,
#             'corneal_thickness_right': corneal_thickness_right,
#             'spherical_left': spherical_left,
#             'spherical_right': spherical_right,
#             'column_left': column_left,
#             'column_right': column_right,
#             'axis_left': axis_left,
#             'axis_right': axis_right,
#             'spherical_equivalent_left': spherical_equivalent_left,
#             'spherical_equivalent_right': spherical_equivalent_right,
#             'suggestion': suggestion,
#         }
#         students.append(student)
# report_str = template.render(students=students)
# pdf = HTML(string=report_str).write_pdf('report.pdf')

print(
    213*None
)