# -*- encoding: utf-8 -*-
"""
@File Name      :   sf.py
@Create Time    :   2022/11/13 19:47
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

import base64
import json
import uuid
from hashlib import md5
from urllib import parse

import requests

from Common.utils.http.exceptions import ParameterError


def call_sf_express_service_by_digital_signatures(
        req_url: str,
        partner_id: str,
        checkword: str,
        request_id: uuid.UUID,
        timestamp: str,
        service_code: str,
        msg_data: dict) -> dict:
    msg_data = json.dumps(msg_data)
    text = parse.quote_plus(msg_data + timestamp + checkword)
    # 先md5加密然后base64加密
    m = md5()
    m.update(text.encode('utf-8'))
    md5_str = m.digest()
    msg_digest = base64.b64encode(md5_str).decode('utf-8')
    data = {
        "partnerID": partner_id,
        "requestID": request_id,
        "serviceCode": service_code,
        "timestamp": timestamp,
        "msgDigest": msg_digest,
        "msgData": msg_data}
    # 发送post请求
    res = requests.post(req_url, data=data, headers={
        "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"
    })
    res_data = json.loads(res.text)
    res_data['apiResultData'] = json.loads(res_data.get('apiResultData', {}))
    if not res_data.get('apiResultData', '{}').get('success', False):
        raise ParameterError(chinese_msg=res_data['apiErrorMsg'], extra=res_data)
    return res_data
