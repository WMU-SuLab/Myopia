"""Manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect, reverse
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

admin.site.site_title = '用户权限管理'
admin.site.site_header = '用户权限管理'


def index_redirect(request):
    # return redirect(reverse('Screening:manage:index'))
    return redirect(reverse('admin:index'))

urlpatterns = [
    path('', index_redirect, name='index'),
    path('user_service/', include('UserService.views', namespace='UserService')),
    path('screening/', include('Screening.views', namespace='Screening')),
    # Django 后台
    path('admin/', admin.site.urls, name='admin'),
    # DRF 提供的一系列身份认证的接口，用于在页面中认证身份，详情查阅DRF文档
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # YOUR PATTERNS，会获得api的yaml文件
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='schema-redoc'),
]
