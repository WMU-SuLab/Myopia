# -*- encoding: utf-8 -*-
"""
@File Name      :   wechat.py    
@Create Time    :   2022/4/12 20:15
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


class WeChatApi:
    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def get_openid_and_session_key(self, code):
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        url = 'https://api.weixin.qq.com/sns/jscode2session'
        r = requests.get(url, params=params)
        return r.json()
