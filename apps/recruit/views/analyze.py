#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated

from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from recruit.utils.decorator import request_log
from django.shortcuts import render
from recruit.utils import response
from recruit import tasks


class AnalysisCharacterView(GenericViewSet):
    serializer_class = serializers.ReportSerializer
    # permission_classes = (IsAuthenticated,)

    @method_decorator(request_log(level='DEBUG'))
    def post(self, request, **kwargs):
        tasks.async_analysis.delay(pk=kwargs["pk"])
        return Response("async_analysis......")

    @method_decorator(request_log(level='DEBUG'))
    def get(self, request, **kwargs):
        try:
            report_obj = models.Report.objects.get(id=kwargs['pk'])
        except Exception as e:
            ret = response.ANALYSIS_DOES_NOT_EXIST
            ret['msg'] += str(e)
            return Response(ret)

        respondenter_name = report_obj.respondenter_name
        wj_name = report_obj.answer.wj.title
        time_consum = report_obj.answer.use_time
        total_scores = json.loads(report_obj.total_scores)
        final_analysis_data = json.loads(report_obj.result)
        anaylze_result = {
            "respondenter_name": respondenter_name,
            "wj_name": wj_name,
            "time_consum": time_consum,
            "total_scores": total_scores,
            "final_analysis_data": final_analysis_data,
        }
        return render(request, 'result_report.html', context={"anaylze_result": anaylze_result})


class ResultView(GenericViewSet):
    """查询所欲分析结果，暂时不使用.

    """

    @method_decorator(request_log(level='DEBUG'))
    def get(self, request):
        final_result = {}
        anaylze_results = models.Report.objects.all()
        for report_obj in anaylze_results:
            respondenter_name = report_obj.respondenter_name
            respondenter_id = report_obj.answer.id
            wj_name = report_obj.answer.wj.title
            time_consum = report_obj.answer.use_time  # 分钟
            total_scores = report_obj.total_scores
            final_analysis_data = report_obj.result
            data = {
                "respondenter_name": respondenter_name,
                "wj_name": wj_name,
                "time_consum": time_consum,
                "total_scores": total_scores,
                "final_analysis_data": final_analysis_data,
            }
            final_result[respondenter_id] = data
        print(final_result)
        return render(request, 'result_report.html', context={"anaylze_result": final_result})