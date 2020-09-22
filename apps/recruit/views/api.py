#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from recruit.utils import response


class WjView(GenericViewSet):
    serializer_class = serializers.WJSerializer
    queryset = models.Wj.objects

    def single(self, request, **kwargs):
        """
        获取单个问卷
        :return:
        """
        new_question = []
        try:
            questions = models.Question.objects.filter(wjId=kwargs['pk']).values()
            obj = self.queryset.get(id=kwargs['pk'])
        except:
            return Response(response.WJ_NOT_EXISTS)

        for q in questions:
            options = models.Options.objects.filter(questionId=q['id']).values()
            q.update(options=[i['title'] for i in options])
            new_question.append(q)

        wj_detail = {
            "name": obj.title,
            "desc": obj.desc,
            "status": obj.status,
            "questions": new_question
        }

        return Response(wj_detail)
