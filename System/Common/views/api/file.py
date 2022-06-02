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

from django.http import FileResponse
from rest_framework.response import Response

from Common.utils.auth.views.api import AllowAnyAPIView
from Common.utils.file_handler.image_handler.thumbnail import make_thumbnail_file_path, make_thumbnail
from Common.utils.http.exceptions import FileNotFound
from Common.utils.text_handler.hash import decrypt_text


class DownloadFileAPIView(AllowAnyAPIView):
    def get(self, request, encrypted_file_text, *args, **kwargs):
        file_path = decrypt_text(encrypted_file_text)
        file_name = os.path.basename(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
        else:
            return Response(FileNotFound())


class DownloadImageAPIView(AllowAnyAPIView):
    def get(self, request, encrypted_file_text, *args, **kwargs):
        file_path = decrypt_text(encrypted_file_text)
        file_name = os.path.basename(file_path)
        if request.GET.get('thumbnail', None):
            width = int(request.GET.get('width', 50))
            height = int(request.GET.get('height', 50))
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
        else:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            else:
                return Response(FileNotFound())
