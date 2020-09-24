#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json

from django.utils.decorators import method_decorator

from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from rest_framework.response import Response
from recruit.utils import response, parser
from recruit.utils.decorator import request_log


class WjView(GenericViewSet):
    serializer_class = serializers.WJSerializer
    queryset = models.Wj.objects

    @method_decorator(request_log(level='DEBUG'))
    def single(self, request, **kwargs):
        """
        获取单个问卷
        :return:
        """
        pk = kwargs['pk']
        try:
            obj = models.Wj.objects.filter(id=pk)
        except:
            return Response(response.WJ_NOT_EXISTS)

        serializer = self.get_serializer(obj, many=True)
        return Response(serializer.data)

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        获取所有问卷
        :param request:
        :return:
        """
        obj = models.Wj.objects.all()
        serializer = self.get_serializer(obj, many=True)

        return Response(serializer.data)


class AnserView(GenericViewSet):
    """
        {
          "submit_answer_id": 1,
          "submit_ip": "172.3.100.101",
          "use_time": 100,
          "wj_id": 1,
          "answer_choice": {
            "1": [1],
            "2": [1,2,3]
          },
          "answer_text": {
            "3": "城南小陌又逢春，只见梅花不见人",
            "4": "人有生老三千疾， 唯有相思不可医！"
          }
    }


    """

    @method_decorator(request_log(level='DEBUG'))
    def post(self, request):
        wj_id = request.data['wj_id']
        submit_user_id = request.data['submit_answer_id']
        submit_ip = request.data.get('submit_ip', '')
        use_time = request.data['use_time']
        answer_choice = json.dumps(request.data.get('answer_choice', ""))
        answer_text = json.dumps(request.data.get('answer_text', ""), ensure_ascii=False)

        try:
            wj = models.Wj.objects.get(id=wj_id)
            submit_user = models.Respondents.objects.get(id=submit_user_id)
        except:
            return Response(response.ANSWER_PARA_ERROR)

        _, tag = models.Answer.objects.update_or_create(
            wj=wj,
            submitIp=submit_ip,
            submitUser=submit_user,
            defaults={
                "answerChoice": answer_choice,
                "answerText": answer_text,
                "useTime": use_time
            }
        )
        answer_sheet = dict(
            submit_user=submit_user.name,
            wj=wj.title,
        )
        if tag:
            answer_sheet.update(response.ANSWER_SAVE_SUCCESS)
            return Response(answer_sheet)
        else:
            answer_sheet.update(response.ANSWER_SAVE_ERROR)
            return Response(answer_sheet)