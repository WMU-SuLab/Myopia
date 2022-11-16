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
from django.utils import timezone

from Common.utils.text_handler.hash import encrypt_text, decrypt_text
from Common.viewModels.cache import get_cache, set_cache
from Sample.models.project import TGFBISampleProject


def encrypt_tgfbi_project(project: TGFBISampleProject):
    return encrypt_text(f'{project.id}-{project.name}')


def decrypt_tgfbi_text(project_text: str):
    text = decrypt_text(project_text)
    if '-' not in text:
        return None
    text_list = text.split('-')
    if text.split('-')[0].isdigit():
        return TGFBISampleProject.objects.get(id=text_list[0], name=text_list[1])
    return None


def send_order_to_lims(project: TGFBISampleProject, serial_number: str):
    date_now = timezone.now().strftime('%Y%m%d')
    id_count_key = f'tgfbi_id_count_{date_now}'
    id_count = get_cache(id_count_key)
    if not id_count:
        id_count = 1
        set_cache(id_count_key, id_count, 60 * 60 * 24)
    else:
        id_count += 1
        set_cache(id_count_key, id_count)
    res = requests.post(url='https://lims.psi-gene.com:8088/rest/RestfulService/submitOrderToCrm', json={
        'sampleOrder': {
            'id': f"JM{date_now}{id_count}",
            'barcode': serial_number,
            'productId': '0102',
            'productName': project.name,
            'samplingDate': project.remarks_json.get('bind_time', None),
            'patientName': project.remarks_json.get('name', None),
            'gender': project.remarks_json.get('gender', ''),
            'birthDate': project.remarks_json.get('birthday', None),
            'phone': project.remarks_json.get('contact_phone_number', None),
            'createDate': project.remarks_json.get('courier', {}).get('update_time'),
            'state': '1',
            'stateName': '完成'
        },
        'file': []
    })

    return res.json()
