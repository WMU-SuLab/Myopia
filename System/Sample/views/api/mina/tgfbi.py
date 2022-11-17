# -*- encoding: utf-8 -*-
"""
@File Name      :   tgfbi.py
@Create Time    :   2022/11/13 15:56
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

from django.utils import timezone
from rest_framework.response import Response

from Common.models.equipments import Sequence
from Common.utils.auth.views.api import IsAuthenticatedAPIView
from Common.utils.auth.views.request_method import HandlePost
from Common.utils.http.exceptions import NotFound, ParameterError, MethodNotAllowed
from Common.utils.http.successes import Success
from Sample.models.project import TGFBISampleProject
from Sample.utils.forms.tgfbi import TGFBISampleBindingForm, TGFBISampleBindingUpdateForm, TGFBISampleSendForm
from Sample.utils.http.sf_express import create_pay_on_arrival_order


class SubmitTGFBISampleBindingFormAPIView(IsAuthenticatedAPIView, HandlePost):
    def create(self, request, *args, **kwargs):
        tgfbi_sample_binding_form = TGFBISampleBindingForm(request.data)
        if not tgfbi_sample_binding_form.is_valid():
            raise ParameterError(msg_detail=tgfbi_sample_binding_form.errors)
        serial_number = tgfbi_sample_binding_form.cleaned_data['serial_number']
        if Sequence.objects.get(serial_number=serial_number):
            raise MethodNotAllowed(chinese_msg='序列号已存在，不允许使用此方法')
        project = TGFBISampleProject.objects.create(
            user=request.user,
            name='TGFBI角膜营养不良基因检测采样',
            progress=1,
            remarks_json=tgfbi_sample_binding_form.cleaned_data,
        )
        Sequence.objects.create(project=project, serial_number=serial_number)
        return Response(Success(chinese_msg='提交样本绑定成功'))

    def patch(self, request, *args, **kwargs):
        tgfbi_sample_binding_form = TGFBISampleBindingUpdateForm(request.data)
        if not tgfbi_sample_binding_form.is_valid():
            raise ParameterError(msg_detail=tgfbi_sample_binding_form.errors)
        project = TGFBISampleProject.objects.prefetch_related('user').get(
            name='TGFBI角膜营养不良基因检测采样',
            sequence__serial_number=tgfbi_sample_binding_form.cleaned_data['serial_number'])
        if not project:
            raise ParameterError(chinese_msg='序列号不存在')
        # 判断用户
        if project.user.username != request.user.username:
            raise ParameterError(chinese_msg='该序列号不属于当前用户')
        project.remarks_json = {**project.remarks_json, **tgfbi_sample_binding_form.cleaned_data}
        project.save()
        return Response(Success(chinese_msg='更新成功'))


class SubmitTGFBISampleSendFormAPIView(IsAuthenticatedAPIView):
    def post(self, request, *args, **kwargs):
        tgfbi_sample_send_form = TGFBISampleSendForm(request.data)
        if not tgfbi_sample_send_form.is_valid():
            raise ParameterError(msg_detail=tgfbi_sample_send_form.errors)
        project = TGFBISampleProject.objects.get(
            user=request.user,
            name='TGFBI角膜营养不良基因检测采样',
            sequence__serial_number=tgfbi_sample_send_form.cleaned_data['serial_number']
        )
        if not project:
            raise NotFound(chinese_msg='该项目不存在')
        if project.progress == 2:
            raise MethodNotAllowed(chinese_msg='已经提交过订单，不允许再提交')
        project.progress = 2
        order_id = f"TGFBI-{timezone.now().strftime('%Y%m%d%H:%M:%S')}-{project.id}"
        sf_res = create_pay_on_arrival_order(
            order_id=order_id,
            contact=tgfbi_sample_send_form.cleaned_data['contact_name'],
            mobile=tgfbi_sample_send_form.cleaned_data['contact_phone_number'],
            province=tgfbi_sample_send_form.cleaned_data['province'],
            city=tgfbi_sample_send_form.cleaned_data['city'],
            county=tgfbi_sample_send_form.cleaned_data['county'],
            address=tgfbi_sample_send_form.cleaned_data['address'],
            send_time=tgfbi_sample_send_form.cleaned_data['send_time'],
            remark=tgfbi_sample_send_form.cleaned_data['remark'],
        )
        project.remarks_json['courier'] = {
            **project.remarks_json.get('courier', {}),
            **tgfbi_sample_send_form.cleaned_data,
            'waybillNoInfoList': sf_res.get('apiResultData', {}).get('msgData', {}).get('waybillNoInfoList', []),
            'update_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sf_express_full_info': sf_res,
        }
        project.save()
        # lims_res = send_order_to_lims(project, tgfbi_sample_send_form.cleaned_data['serial_number'])
        # project.remarks_json['lims_full_info'] = lims_res
        # project.save()
        return Response(Success(chinese_msg='提交寄件成功', extra=sf_res))
