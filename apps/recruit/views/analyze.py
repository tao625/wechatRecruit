#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import random
from django.utils.decorators import method_decorator
from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from recruit.utils import response, parser
from recruit.utils.decorator import request_log
from wechatRecruit import pagination
from recruit.utils import character_analysis
from django.shortcuts import render


class AnalysisCharacterView(GenericViewSet):

    def get(self, request, **kwargs):
        """获取答卷分析结果

        :param request:
        :param kwargs: 答卷ID
        :return:
        """
        anaylze_result = {}
        answer_id = kwargs['pk']
        obj = character_analysis.AnalyzeCharacter()
        result = obj.execute(pk=answer_id)
        try:
            answer = models.Answer.objects.get(id=answer_id)
        except:
            return Response(response.ANSWER_NOT_EXIST)
        analyze_data = models.AnalysisData.objects.filter(wj=answer.wj.id).values('content', 'tags')
        contrast = {}
        for per in analyze_data:
            animal_id = per['tags']
            content = per['content']
            name = models.Animal.objects.get(id=animal_id).name
            val = contrast.get(content)
            if val:
               val.append(name)
            else:
                contrast[content] = [name]

        for c, t in contrast.items():
            if set(t) == set(result.keys()):
                anaylze_result['job'] = c
            else:
                anaylze_result['job'] = ""

        data = {}
        for k in result.keys():
            feature = models.Animal.objects.get(name=k, wj=answer.wj.id).feature
            num = str(random.randint(1, 3))
            data[k] = [feature, num]

        anaylze_result['features'] = data
        return render(request, 'result_report.html', context={"anaylze_result": anaylze_result})