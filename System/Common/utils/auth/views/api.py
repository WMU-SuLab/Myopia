# -*- encoding: utf-8 -*-
"""
@File Name      :   api.py    
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

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from Common.utils.auth.permissions import DjangoModelPermissions


class AllowAnyAPIView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)


class AllowAnyGenericAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)


class IsAuthenticatedAPIView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated,)


class IsAuthenticatedGenericAPIView(GenericAPIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated, DjangoModelPermissions)


class IsAuthenticatedOrReadOnlyAPIView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IsAuthenticatedOrReadOnlyGenericAPIView(GenericAPIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissions)


class AdminIsAuthenticatedAPIView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)


class AdminIsAuthenticatedGenericAPIView(GenericAPIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser, DjangoModelPermissions)
