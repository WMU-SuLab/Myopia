# -*- encoding: utf-8 -*-
"""
@File Name      :   sample.py    
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

from Common.models.user import User, Nationality
from Common.utils.text_handler.validator import validate_phone


class SampleForm(forms.Form):
    serial_number = forms.CharField(min_length=9)
    # person info
    name = forms.CharField(max_length=32)
    gender = forms.CharField()
    age = forms.IntegerField(required=False)
    birthday = forms.DateField()
    native_place = forms.CharField(max_length=32)
    contact_phone = forms.CharField(validators=[validate_phone])
    nationality = forms.CharField(max_length=20)
    education = forms.IntegerField()
    # eye info
    wear_glasses_first_time = forms.CharField()
    optometry_left = forms.CharField()
    optometry_right = forms.CharField()

    family_history = forms.CharField(max_length=1024)
    # 知情同意书
    informed_consent_file = forms.FileField(required=False)

    def clean_education(self):
        education = self.cleaned_data['education']
        if education not in [education[0] for education in User.education_choices]:
            raise forms.ValidationError('教育程度不合法')
        return education

    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality', Nationality)
        if not Nationality.objects.filter(name=nationality).exists():
            raise forms.ValidationError('民族输入错误')
        return nationality
