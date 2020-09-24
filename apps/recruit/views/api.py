#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json

from django.utils.decorators import method_decorator

from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from recruit.utils import response, parser
from recruit.utils.decorator import request_log
from wechatRecruit import pagination


class WjView(GenericViewSet):
    serializer_class = serializers.WJSerializer
    pagination_class = pagination.MyCursorPagination
    permission_classes = (DjangoModelPermissions,)
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


class AnswerView(GenericViewSet, mixins.ListModelMixin):
    """
        {
          "submit_user_id": 1,
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
    serializer_class = serializers.AnswerSerializer
    pagination_class = pagination.MyCursorPagination
    permission_classes = (DjangoModelPermissions,)
    queryset = models.Answer.objects

    @method_decorator(request_log(level='DEBUG'))
    def post(self, request):
        """
        保存答卷
        :param request:
        :return:
        """

        wj_id = request.data['wj_id']
        submit_user_id = request.data['submit_user_id']
        submit_ip = request.data.get('submit_ip', '')
        use_time = request.data['use_time']
        answer_choice = json.dumps(request.data.get('answer_choice', ""))
        answer_text = json.dumps(request.data.get('answer_text', ""), ensure_ascii=False)

        try:
            wj = models.Wj.objects.get(id=wj_id)
            submit_user = models.Respondents.objects.get(id=submit_user_id)
        except:
            return Response(response.ANSWER_PARA_ERROR)

        data = {
            'wj': wj,
            'submit_ip': submit_ip,
            'submit_user': submit_user,
            'answer_choice': answer_choice,
            'answer_text': answer_text,
            'use_time': use_time
        }
        answer_sheet = dict(
            submit_user=submit_user.name,
            wj=wj.title,
        )
        s = self.get_serializer(data=data)
        if s.is_valid():
            s.save(wj=wj, submit_user=submit_user)
            answer_sheet.update(response.ANSWER_SAVE_SUCCESS)
            return Response(answer_sheet)
        else:
            answer_sheet.update(response.ANSWER_SAVE_ERROR)
            return Response(answer_sheet)

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        展示所有答题卡
        :param request:
        :return:
        """

        querset = self.get_queryset()
        serializer = self.get_serializer(querset, many=True)

        return Response(serializer.data)

    @method_decorator(request_log(level='DEBUG'))
    def single(self, request, **kwargs):
        """
        查询指定答卷
        :param request:
        :param kwargs: pk
        :return:
        """

        try:
            queryset = self.queryset.filter(id=kwargs['pk'])
        except:
            return Response(response.ANSWER_NOT_EXIST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RespondentsView(GenericViewSet, mixins.ListModelMixin):
    """
    应聘者信息
    """

    pagination_class = pagination.MyCursorPagination
    permission_classes = (DjangoModelPermissions,)
    serializer_class = serializers.RespondentsSerializer
    queryset = models.Respondents.objects

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            try:
                respondent = self.queryset.filter(id=user_id)
            except:
                return Response(response.RESPONDENT_NOT_EXIST)
        else:
            respondent = self.get_queryset()

        s = self.get_serializer(respondent, many=True)
        return Response(s.data)

