# -*- encoding: utf-8 -*-
"""
@File Name      :   fiole.py    
@Create Time    :   2022/5/26 22:02
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

import os

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from rest_framework.response import Response

from Common.utils.alibabacloud.oss.obj import is_obj_file_path, parsing_obj_file_path, obj_sign_url, download_obj, \
    obj_exist
from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.file_handler.image_handler.thumbnail import make_thumbnail_file_path, make_thumbnail
from Common.utils.http.exceptions import FileNotFound
from Common.utils.text_handler.hash import decrypt_text


@method_decorator(gzip_page, name="dispatch")
class DownloadFileAPIView(AllowAnyAPIView):
    def get(self, request, encrypted_file_text, *args, **kwargs):
        file_path = decrypt_text(encrypted_file_text)
        if is_obj_file_path(file_path):
            obj_file_path = parsing_obj_file_path(file_path)
            if obj_exist(obj_file_path):
                return redirect(obj_sign_url(obj_file_path, 60))
            else:
                raise FileNotFound(obj_file_path)
        else:
            file_name = os.path.basename(file_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            else:
                return Response(FileNotFound())


@method_decorator(gzip_page, name="dispatch")
class DownloadImageAPIView(AllowAnyAPIView):
    def handle_thumbnail(self, file_path, width, height):
        thumbnail_file_path = make_thumbnail_file_path(file_path, width=width, height=height)
        thumbnail_file_name = os.path.basename(thumbnail_file_path)
        if os.path.exists(thumbnail_file_path) and os.path.isfile(thumbnail_file_path):
            return FileResponse(open(thumbnail_file_path, 'rb'), as_attachment=True, filename=thumbnail_file_name)
        else:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                thumbnail_file_path = make_thumbnail(file_path=file_path, width=width, height=height)
                if os.path.exists(thumbnail_file_path) and os.path.isfile(thumbnail_file_path):
                    return FileResponse(open(thumbnail_file_path, 'rb'), as_attachment=True,
                                        filename=thumbnail_file_name)
                else:
                    return Response(FileNotFound())
            else:
                return Response(FileNotFound())

    def get(self, request, encrypted_file_text, *args, **kwargs):
        file_path = decrypt_text(encrypted_file_text)
        if is_obj_file_path(file_path):
            obj_file_path = parsing_obj_file_path(file_path)
            if request.GET.get('thumbnail', None):
                local_file_path = os.path.join(settings.USER_IMAGES_DIR_PATH, obj_file_path)
                download_obj(obj_file_path, local_file_path)
                width = int(request.GET.get('width', 50))
                height = int(request.GET.get('height', 50))
                return self.handle_thumbnail(local_file_path, width, height)
            else:
                if obj_exist(obj_file_path):
                    return redirect(obj_sign_url(obj_file_path, 60))
                else:
                    return Response(FileNotFound())
        else:
            file_name = os.path.basename(file_path)
            if request.GET.get('thumbnail', None):
                width = int(request.GET.get('width', 50))
                height = int(request.GET.get('height', 50))
                return self.handle_thumbnail(file_path, width, height)
            else:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
                else:
                    return Response(FileNotFound())
