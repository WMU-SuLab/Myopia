# -*- encoding: utf-8 -*-
"""
@File Name      :   sf_express.py
@Create Time    :   2022/11/14 17:37
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

from rest_framework.response import Response

from Common.utils.auth.views.api import IsAuthenticatedAPIView
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import Success
from Sample.utils.http.sf_express import cancel_order


class CancelSFExpressAPIView(IsAuthenticatedAPIView):
    def post(self, request, order_id, *args, **kwargs):
        res = cancel_order(order_id)
        if not res.get('apiResultData', '{}').get('success', False):
            raise ParameterError(chinese_msg=res['apiErrorMsg'], extra=res)
        return Response(Success('取消寄件成功', extra=res))
