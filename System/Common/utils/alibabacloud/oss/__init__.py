# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py.py    
@Create Time    :   2022/7/10 18:20
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

import oss2
from django.conf import settings

from Common.utils.http.exceptions import ServerError, ParameterError

access_key_id = settings.ALIBABACLOUD_OSS_ACCESS_KEY_ID
access_key_secret = settings.ALIBABACLOUD_OSS_ACCESS_KEY_SECRET
endpoint = settings.ALIBABACLOUD_OSS_ENDPOINT
bucket_name = settings.ALIBABACLOUD_OSS_BUCKET_NAME


auth = oss2.Auth(access_key_id, access_key_secret)

bucket = oss2.Bucket(
    auth,
    endpoint,
    bucket_name,
    # 设置连接超时
    connect_timeout=30,
    # 设置enable_crc=False来关闭CRC数据校验。
    enable_crc=False
)


def handle_oss_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # ClientError是由于客户端输入有误引起的
        # ClientError的status值是oss2.exceptions.OSS_CLIENT_ERROR_STATUS
        # 例如，使用bucket.batch_delete_objects方法时，如果收到空的文件列表，会抛出该异常
        except oss2.exceptions.ClientError as e:
            raise ParameterError(msg_detail=str(e))
        # 当HTTP库抛出异常时，PythonSDK会将其转换为RequestError
        # RequestError的status值是oss2.exceptions.OSS_REQUEST_ERROR_STATUS
        except oss2.exceptions.RequestError as e:
            raise ParameterError(msg_detail=str(e))
        # 当OSS服务器返回HTTP错误码时，PythonSDK会将其转换为ServerError。
        # ServerError根据HTTP状态码和OSS错误码派生出多个子类。其中NotFound子类对应所有404异常，Conflict子类对应所有409异常
        except oss2.exceptions.ServerError as e:
            raise ServerError(msg_detail=str(e))
        except Exception as e:
            raise ServerError(msg_detail=str(e))

    return wrapper
