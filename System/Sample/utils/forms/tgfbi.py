# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/13 17:34
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

from Common.libs.choices import gender_choices, identification_card_type_choices
from Common.utils.forms.validators import phone_number_validators
from Common.viewModels.choices import same_choices
from . import serial_number


class TGFBISampleBindingForm(forms.Form):
    serial_number = serial_number
    name = forms.CharField(label='姓名', max_length=32)
    gender = forms.ChoiceField(label='性别', choices=same_choices(gender_choices))
    birthday = forms.DateField(label='出生日期', input_formats=['%Y-%m-%d'])
    bind_time = forms.DateTimeField(label='绑定时间', input_formats=['%Y-%m-%d %H:%M:%S'])
    contact_phone_number = forms.CharField(label='手机号', validators=phone_number_validators, required=False)
    identification_card_type = forms.ChoiceField(
        label='证件类型', choices=same_choices(identification_card_type_choices), required=False)
    identification_card_number = forms.CharField(label='证件号码', max_length=32, required=False)
    body_part = forms.ChoiceField(label='采集身体部位', choices=['生殖器', '肛门', '口腔'], required=False)

    def clean_birthday(self):
        return self.cleaned_data['birthday'].strftime('%Y-%m-%d')

    def clean_bind_time(self):
        return self.cleaned_data['bind_time'].strftime('%Y-%m-%d %H:%M:%S')


class TGFBISampleBindingUpdateForm(TGFBISampleBindingForm):
    serial_number = serial_number
    name = forms.CharField(label='姓名', max_length=32, required=False)
    gender = forms.ChoiceField(label='性别', choices=same_choices(gender_choices), required=False)
    birthday = forms.DateField(label='出生日期', input_formats=['%Y-%m-%d'], required=False)


class TGFBISampleSendForm(forms.Form):
    serial_number = serial_number
    contact_name = forms.CharField(label='联系人姓名', max_length=32)
    contact_phone_number = forms.CharField(label='联系电话', validators=phone_number_validators)
    province = forms.CharField(label='省份', max_length=32)
    city = forms.CharField(label='城市', max_length=32)
    county = forms.CharField(label='区县', max_length=32)
    address = forms.CharField(label='详细地址', max_length=128)
    send_time = forms.DateTimeField(label='寄送时间', input_formats=['%Y-%m-%d %H:%M:%S'])
    remark = forms.CharField(label='备注', max_length=256, required=False)

    def clean_send_time(self):
        return self.cleaned_data['send_time'].strftime('%Y-%m-%d %H:%M:%S')


class TGFBIReportForm(forms.Form):
    encrypted_text = forms.CharField(label='加密数据', max_length=1024)
    report_file = forms.FileField(label='报告文件')
