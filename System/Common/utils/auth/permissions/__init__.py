# -*- encoding: utf-8 -*-
"""
@File Name      :   __init__.py
@Create Time    :   2022/5/23 10:45
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

from django.contrib.auth import get_permission_codename
from django.db.models import Model
from rest_framework.permissions import BasePermission, DjangoModelPermissions as _DjangoModelPermissions, \
    DjangoModelPermissionsOrAnonReadOnly as _DjangoModelPermissionsOrAnonReadOnly, \
    DjangoObjectPermissions as _DjangoObjectPermissions

add_get_perms_map = {
    'GET': ['%(app_label)s.view_%(model_name)s'],
    'OPTIONS': [],
    'HEAD': [],
    'POST': ['%(app_label)s.add_%(model_name)s'],
    'PUT': ['%(app_label)s.change_%(model_name)s'],
    'PATCH': ['%(app_label)s.change_%(model_name)s'],
    'DELETE': ['%(app_label)s.delete_%(model_name)s'],
}


class DjangoModelPermissions(_DjangoModelPermissions):
    perms_map = add_get_perms_map


class DjangoModelPermissionsOrAnonReadOnly(_DjangoModelPermissionsOrAnonReadOnly):
    perms_map = add_get_perms_map


class DjangoObjectPermissions(_DjangoObjectPermissions):
    perms_map = add_get_perms_map


class ModelPermission(BasePermission):
    model: Model = None


class ModelViewPermission(ModelPermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            get_permission_codename('view', self.model._meta)
        )


class ModelAddPermission(ModelPermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            get_permission_codename('add', self.model._meta)
        )


class ModelChangePermission(ModelPermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            get_permission_codename('change', self.model._meta)
        )


class ModelDeletePermission(ModelPermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            get_permission_codename('delete', self.model._meta)
        )
