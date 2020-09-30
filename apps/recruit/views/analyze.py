#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
from django.utils.decorators import method_decorator
from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from recruit.utils import response
from recruit.utils.decorator import request_log
from django.shortcuts import render
from recruit import tasks


class AnalysisCharacterView(GenericViewSet):
    serializer_class = serializers.ReportSerializer

    @method_decorator(request_log(level='DEBUG'))
    def post(self, request, **kwargs):
        tasks.async_analysis.delay(pk=kwargs["pk"])
        return Response("测试 async_analysis")

    @method_decorator(request_log(level='DEBUG'))
    def get(self, request, **kwargs):
        try:
            answer = models.Answer.objects.get(id=kwargs['pk'])
            result = models.Report.objects.get(id=answer.report.id).result
        except:
            return Response(response.REPORT_NOT_EXIST)

        anaylze_result = json.loads(result)

        return render(request, 'result_report.html', context={"anaylze_result": anaylze_result})