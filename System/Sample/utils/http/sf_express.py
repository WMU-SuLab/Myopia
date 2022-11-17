# -*- encoding: utf-8 -*-
"""
@File Name      :   sf.py
@Create Time    :   2022/11/13 21:09
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

import time
import uuid

from django.conf import settings

from Common.utils.http.sf_express import call_sf_express_service_by_digital_signatures


def base_config():
    req_url = settings.SF_EXPRESS_URL
    partner_id = settings.SF_EXPRESS_SAMPLE_APP_PARTNER_ID
    checkword = settings.SF_EXPRESS_SAMPLE_APP_CHECKWORD
    # 生成uuid
    request_id = uuid.uuid1()
    # 获取时间戳
    timestamp = str(int(time.time()))
    return req_url, partner_id, checkword, request_id, timestamp


def create_pay_on_arrival_order(
        order_id: str,
        contact: str,
        mobile: str,
        province: str,
        city: str,
        county: str,
        address: str,
        send_time: str,
        remark: str = '',
) -> dict:
    return call_sf_express_service_by_digital_signatures(
        *base_config(),
        service_code='EXP_RECE_CREATE_ORDER',
        msg_data={
            'language': 'zh-CN',
            # 客户订单号
            'orderId': order_id,
            # 托寄物信息
            'cargoDetails': [{
                'name': '口腔拭子采样样本',
                'count': 1,
                'unit': '件',
            }],
            # 收寄双方信息
            'contactInfoList': [{
                # 寄件方信息
                'contactType': 1,
                'contact': contact,
                'mobile': mobile,
                'zoneCode': 'CN',
                'country': '中国',
                'province': province,
                'city': city,
                'county': county,
                'address': address,
            }, {
                # 收件方信息
                'contactType': 2,
                'company': '温州谱希医学检验实验室有限公司',
                'contact': '收样员',
                'mobile': '',
                'tel': '0577-56651101',
                'zoneCode': 'CN',
                'country': '中国',
                'province': '浙江省',
                'city': '温州市',
                'county': '龙湾区',
                'address': '浙江省温州市龙湾区永中街道中国眼谷3栋一楼',
                'postCode': '325000',
                'email': '',
                'taxNo': '',
            }],
            # 要求上门取件开始时间，格式：YYYY-MM-DD HH24:MM:SS
            'sendStartTm': send_time,
            # 付款方式
            'payMethod': 2,
            # 快件产品类别，参考https://open.sf-express.com/developSupport/734349?activeIndex=324604
            'expressTypeId': 2,
            # 是否返回路由标签： 默认1， 1：返回路由标签， 0：不返回；
            'isReturnRoutelabel': 1,
            # 是否需求分配运单号，1：分配，0：不分配（若带单号下单，请传值0）
            'isGenWaybillNo': 1,
            # 备注
            'remark': remark,
        }
    )


def cancel_order(order_id):
    return call_sf_express_service_by_digital_signatures(
        *base_config(),
        service_code='EXP_RECE_UPDATE_ORDER',
        msg_data={
            "dealType": 2,
            "language": "zh-CN",
            "orderId": order_id
        }
    )
