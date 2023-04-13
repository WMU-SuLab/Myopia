# -*- encoding: utf-8 -*-
"""
@File Name      :   gunicorn.py    
@Create Time    :   2022/4/4 16:28
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

import multiprocessing
import os

from Config.settings.project import BASE_DIR, GUNICORN_LOGS_DIR_PATH, SERVER_DOMAIN, SERVER_PORT

# 绑定ip和端口号
ip = SERVER_DOMAIN or '0.0.0.0'
port = SERVER_PORT or '8000'
bind = [f'{ip}:{port}', f'[::1]:{port}']
# 进程名
proc_name = 'myopia_gunicorn_process'
# 监听队列
backlog = 512
# gunicorn要切换到的目的工作目录
chdir = str(BASE_DIR)
# 超时
timeout = 30
# 超时重启
graceful_timeout = 300
# 在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间。
keepalive = 3
# HTTP请求行的最大大小，此参数用于限制HTTP请求行的允许大小，默认情况下，这个值为4094。
# 值是0~8190的数字。此参数可以防止任何DDOS攻击
limit_request_line = 4096
# 限制HTTP请求中请求头字段的数量。
#  此字段用于限制请求头字段的数量以防止DDOS攻击，与limit-request-field-size一起使用可以提高安全性。
# 默认情况下，这个值为100，这个值不能超过32768
limit_request_fields = 100
# 限制HTTP请求中请求头的大小，默认情况下这个值为8190。
# 值是一个整数或者0，当该值为0时，表示将对请求头大小不做限制
limit_request_field_size = 8190
# 设置守护进程(linux有效)，请注意使用 supervisor 的时候不能后台运行
# daemon = 'true'
daemon = 'false'
# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'gevent'
# 进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 指定每个进程开启的线程数
threads = 3
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 访问日志文件
accesslog = os.path.join(GUNICORN_LOGS_DIR_PATH, "access.log")
# 错误日志文件
errorlog = os.path.join(GUNICORN_LOGS_DIR_PATH, "error.log")
