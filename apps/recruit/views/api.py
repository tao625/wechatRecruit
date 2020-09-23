#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from recruit.utils import response, parser


class WjView(GenericViewSet):
    serializer_class = serializers.WJSerializer
    queryset = models.Wj.objects

    def single(self, request, **kwargs):
        """
        获取单个问卷
        :return:
        """
        pk = kwargs['pk']
        try:
            obj = models.Wj.objects.get(id=pk)
        except:
            return Response(response.WJ_NOT_EXISTS)

        questions = parser.get_question_detail(pk)

        wj_detail = {
            "name": obj.title,
            "desc": obj.desc,
            "status": obj.status,
            "questions": questions
        }

        return Response(wj_detail)


    def list(self, request):
        result = []
        wjs = self.queryset.all().values('id', 'title', 'desc', 'status')
        for wj in wjs:
            detail_wj = parser.get_question_detail(wj['id'])
            wj_detail = {
                "name": wj['title'],
                "desc": wj['desc'],
                "status": wj['status'],
                "questions": detail_wj
            }
            result.append(wj_detail)

        return Response(result)

