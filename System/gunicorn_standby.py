# -*- encoding: utf-8 -*-
"""
@File Name      :   gunicorn_extra.py
@Create Time    :   2022/11/19 20:08
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

from gunicorn import *

port_standby = 8001
bind = f"{ip}:{port_standby}"
# 访问日志文件
accesslog = os.path.join(GUNICORN_LOGS_DIR_PATH, "access_standby.log")
# 错误日志文件
errorlog = os.path.join(GUNICORN_LOGS_DIR_PATH, "error_standby.log")
