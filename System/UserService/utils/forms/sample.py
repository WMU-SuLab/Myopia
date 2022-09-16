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
from django.core.validators import RegexValidator

from Common.models.user import User, Nationality
from Common.utils.text_handler.validator import validate_phone_number


class SampleForm(forms.Form):
    serial_number = forms.CharField(min_length=9, validators=[
        RegexValidator(regex=r'\d{2}[A-Z]{2}[A-Za-z0-9]{5,12}', message='序列号规则验证错误，不是合法的序列号', code='invalid serial_number'),
    ])
    # person info
    name = forms.CharField(max_length=32)
    gender = forms.CharField()
    age = forms.IntegerField(required=False)
    birthday = forms.DateField()
    native_place = forms.CharField(max_length=32)
    contact_phone = forms.CharField(validators=[validate_phone_number])
    nationality = forms.CharField(max_length=20)
    education = forms.CharField()
    # eye info
    wear_glasses_first_time = forms.CharField()
    optometry_left = forms.CharField()
    optometry_right = forms.CharField()

    family_history = forms.CharField(max_length=1024, required=False)
    # 知情同意书
    informed_consent_file = forms.FileField()

    def clean_education(self):
        education = self.cleaned_data['education']
        if education and education not in [education[1] for education in User.education_choices]:
            raise forms.ValidationError('教育程度不合法')
        return education

    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality', Nationality)
        if nationality and not Nationality.objects.filter(name=nationality).exists():
            raise forms.ValidationError('民族输入错误')
        return nationality

    def clean_birthday(self):
        return self.cleaned_data['birthday'].strftime('%Y-%m-%d')


class SampleFormUpdate(SampleForm):
    informed_consent_file = forms.FileField(required=False)


class SampleManageForm(forms.Form):
    project_id = forms.IntegerField()
    progress = forms.IntegerField()
