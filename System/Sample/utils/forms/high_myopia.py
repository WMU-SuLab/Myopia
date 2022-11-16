# -*- encoding: utf-8 -*-
"""
@File Name      :   high_myopia.py
@Create Time    :   2022/6/1 10:31
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

from django import forms

from Common.libs.choices import education_choices
from Common.models.user import Nationality
from Common.utils.forms.validators import phone_number_validators
from Common.viewModels.choices import choices_to_list
from . import serial_number


class HighMyopiaForm(forms.Form):
    serial_number = serial_number
    # person info
    name = forms.CharField(label='姓名', max_length=32)
    gender = forms.CharField(label='性别')
    age = forms.IntegerField(required=False)
    birthday = forms.DateField(label='出生日期', input_formats=['%Y-%m-%d'])
    native_place = forms.CharField(max_length=32)
    contact_phone = forms.CharField(validators=phone_number_validators)
    nationality = forms.CharField(max_length=20)
    education = forms.CharField()
    # eye info
    wear_glasses_first_time = forms.CharField()
    optometry_left = forms.CharField()
    optometry_right = forms.CharField()

    family_history = forms.CharField(max_length=1024, required=False)
    # 知情同意书
    informed_consent_file = forms.FileField(required=False)

    def clean_education(self):
        education = self.cleaned_data['education']
        if education and education not in choices_to_list(education_choices):
            raise forms.ValidationError('教育程度不合法')
        return education

    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality', Nationality)
        if nationality and not Nationality.objects.filter(name=nationality).exists():
            raise forms.ValidationError('民族输入错误')
        return nationality

    def clean_birthday(self):
        return self.cleaned_data['birthday'].strftime('%Y-%m-%d')


class HighMyopiaFormUpdate(HighMyopiaForm):
    informed_consent_file = forms.FileField(required=False)


class HighMyopiaManageForm(forms.Form):
    project_id = forms.IntegerField()
    progress = forms.IntegerField()
