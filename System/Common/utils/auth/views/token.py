# -*- encoding: utf-8 -*-
"""
@File Name      :   token.py    
@Create Time    :   2022/4/29 10:48
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

from datetime import datetime

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView as _TokenObtainPairView, \
    TokenRefreshView as _TokenRefreshView, \
    TokenVerifyView as _TokenVerifyView, TokenBlacklistView as _TokenBlacklistView, \
    TokenObtainSlidingView as _TokenObtainSlidingView, TokenRefreshSlidingView as _TokenRefreshSlidingView

from Common.serializers.token import TokenObtainPairSerializer, TokenRefreshSerializer, TokenVerifySerializer, \
    TokenBlacklistSerializer, TokenObtainSlidingSerializer, TokenRefreshSlidingSerializer
from Common.utils.http.exceptions import TokenNotExist


class RequestMutableMixin:
    @staticmethod
    def set_mutable_request_data(request):
        if type(request.data) == dict:
            pass
        else:
            setattr(request.data, '_mutable', True)
        return request


# 全部改造为 HTTP Only 的方式，如果需要切换回来，将所有的 get 和 post 方法注释即可
class TokenObtainPairView(_TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh', None)
        refresh_expire_at = response.data.pop('refresh_expire_at', 0)
        if refresh:
            refresh_expires = int((datetime.fromtimestamp(refresh_expire_at) - datetime.now()).total_seconds())
            response.set_cookie('refresh', refresh, max_age=refresh_expires, expires=refresh_expires, httponly=True)
        return response


class TokenRefreshView(_TokenRefreshView, RequestMutableMixin):
    serializer_class = TokenRefreshSerializer

    def get(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh', None)
        if refresh:
            request = self.set_mutable_request_data(request)
            request.data['refresh'] = refresh
            return super().post(request, *args, **kwargs)
        else:
            return Response(TokenNotExist())


class TokenVerifyView(_TokenVerifyView, RequestMutableMixin):
    serializer_class = TokenVerifySerializer

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        token = request.data.get('token', None)
        if token:
            return super().post(request, *args, **kwargs)
        token = request.COOKIES.get('refresh', None)
        if token:
            request = self.set_mutable_request_data(request)
            request.data['token'] = token
            return super().post(request, *args, **kwargs)
        return Response(TokenNotExist())


class TokenBlacklistView(_TokenBlacklistView, RequestMutableMixin):
    serializer_class = TokenBlacklistSerializer

    def get(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh', None)
        if refresh:
            request = self.set_mutable_request_data(request)
            request.data['refresh'] = refresh
            response = super().post(request, *args, *kwargs)
            response.delete_cookie('refresh')
            return response
        refresh = request.data.get('refresh', None)
        if refresh:
            return super().post(request, *args, *kwargs)
        return Response(TokenNotExist(msg_detail='None refresh token'))


class TokenObtainSlidingView(_TokenObtainSlidingView, RequestMutableMixin):
    serializer_class = TokenObtainSlidingSerializer


class TokenRefreshSlidingView(_TokenRefreshSlidingView, RequestMutableMixin):
    serializer_class = TokenRefreshSlidingSerializer
