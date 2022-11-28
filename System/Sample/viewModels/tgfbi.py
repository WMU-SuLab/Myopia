# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/15 21:48
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

import requests
from django.conf import settings

from Common.utils.http.exceptions import ServerError, ValidationError
from Common.utils.text_handler.hash import encrypt_text, decrypt_text
from Sample.models.project import TGFBISampleProject


def encrypt_tgfbi_project(project: TGFBISampleProject):
    return encrypt_text(f'{project.id}-{project.name}')


def decrypt_tgfbi_text(encrypted_text: str) -> TGFBISampleProject or None:
    text = decrypt_text(encrypted_text)
    if '-' not in text:
        return None
    text_list = text.split('-')
    project_id = text_list[0]
    project_name = text_list[1]
    if project_id.isdigit():
        return TGFBISampleProject.objects.get(id=project_id, name=project_name)
    return None


def send_order_to_lims(project: TGFBISampleProject, serial_number: str):
    encrypted_text = encrypt_tgfbi_project(project)
    if 'JMF' in serial_number:
        project_id = 'PSI20220003JMF'
        product_name = '角膜营养不良检测-基础版'
    elif 'JMA' in serial_number:
        project_id = 'PSI20220004JMA'
        product_name = '角膜营养不良检测-基础版'
    else:
        raise ValidationError(chinese_msg='无效的样本编号', msg_detail='样本编号不包含JMF或JMA')
    sample_order = {
        'barcode': serial_number,
        'projectId': project_id,
        'productId': '0102',
        'productName': product_name,
        'samplingDate': project.remarks_json.get('bind_time', None),
        'patientName': project.remarks_json.get('name', None),
        'gender': project.remarks_json.get('gender', ''),
        'birthDate': project.remarks_json.get('birthday', None),
        'phone': project.remarks_json.get('contact_phone_number', None),
        'patientNation': '汉族',
        'dioptric': '',
        'leftEye': '',
        'rightEye': '',
        'astigmatism': '',
        'leftAdjust': '',
        'rightAdjust': '',
        'createDate': project.remarks_json.get('courier', {}).get('update_time'),
    }
    form_data = {
        'sampleOrder': sample_order,
        'encrypted_text': encrypted_text,
    }
    res = requests.post(url=settings.SAMPLE_APP_LIMS_TGFBI_URL, files={
        'formData': (None, str(form_data)),
    })
    try:
        res_data = res.json()
    except Exception as e:
        raise ServerError(msg=str(e), chinese_msg='LIMS服务器返回数据格式错误' + res.text)
    if not res_data.get('success', False):
        raise ServerError(chinese_msg='提交LIMS系统订单出错', extra=res_data)
    return {**res_data, 'form_data': form_data}
