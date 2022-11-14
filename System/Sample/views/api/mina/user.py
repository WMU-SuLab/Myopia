# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py
@Create Time    :   2022/11/11 21:17
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

from Common.utils.alibabacloud.sms.verification import send_verification_sms
from Common.utils.http.exceptions import ParameterError
from Common.utils.http.successes import PhoneSMSSendSuccess
from Common.views.api.user import SendPhoneSMSAPIView as _SendPhoneSMSAPIView


class SendPhoneSMSAPIView(_SendPhoneSMSAPIView):
    def post(self, request):
        usage = request.GET.get('usage', None)
        if not usage:
            raise ParameterError(msg_detail='usage field is required')
        data = send_verification_sms(self.validate(request), '谱希基因', 'SMS_244615604', usage)
        return Response(PhoneSMSSendSuccess(data=data))
