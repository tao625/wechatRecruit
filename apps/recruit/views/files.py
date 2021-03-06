#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from recruit import serializers
from rest_framework import mixins
from recruit import models
from recruit.utils import upload
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from wechatRecruit.settings import MEDIA_ROOT
from . import logger
from django.shortcuts import render
from recruit.utils import response


class FileView(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.FileSerializer
    queryset = models.UploadFile.objects

    def create(self, request, **kwargs):
        if not request.FILES:
            return Response(response.NOT_FOUND_EXCEL)
        request.data['create_by'] = request.user.id
        request.data['name'] = request.FILES['file'].name
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self.kwargs['pk'] = obj.id
        instance = self.get_object()
        path = os.path.normpath(os.path.join(MEDIA_ROOT, str(instance.file)))
        logger.info({'data': request.data, 'file': path})
        if os.path.exists(path):
            upload.get_data.delay(path, id=obj.id)
        ret = response.UPLOAD_EXCEL_FILE
        ret.update(**serializer.data)
        ret.update(create_by=request.user.username)
        return Response(ret)

    def get(self, request):
        return render(request, 'upload_excel.html')