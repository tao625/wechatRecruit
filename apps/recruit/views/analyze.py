#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.utils.decorators import method_decorator

from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from recruit.utils import response, parser
from recruit.utils.decorator import request_log
from wechatRecruit import pagination
from recruit.utils import character_analysis


class AnalysisCharacter(GenericViewSet):

    def post(self, request, **kwargs):
        """获取答卷分析结果

        :param request:
        :param kwargs: 答卷ID
        :return:
        """
        answer_id = kwargs['pk']
        obj = character_analysis.AnalyzeCharacter()
        result = obj.execute(pk=answer_id)
