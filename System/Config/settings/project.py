# -*- encoding: utf-8 -*-
"""
@File Name      :   project.py    
@Create Time    :   2022/4/15 10:23
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

from .base import *

# Project settings
SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN', 'localhost')
# Screening-Manage
SimpleUI = {

}

# MINA
mina = {
    'screening': {
        'appid': os.environ.get('MINA_SCREENING_APPID', None),
        'app_secret': os.environ.get('MINA_SCREENING_APP_SECRET', None),
    },
    'user_service': {
        'appid': os.environ.get('MINA_USER_SERVICE_APPID', None),
        'app_secret': os.environ.get('MINA_USER_SERVICE_APP_SECRET', None),
    },
}
