#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json


from . import logger
from django.utils.decorators import method_decorator

from recruit import serializers, models
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from recruit.utils import response
from recruit.utils.base_return import BaseResponse
from recruit.utils.decorator import request_log
from wechatRecruit import pagination
from recruit import tasks
from ..utils.permissions import CheckTokenPermission


class WjView(GenericViewSet):
    serializer_class = serializers.WJSerializer
    pagination_class = pagination.MyCursorPagination
    queryset = models.Wj.objects
    permission_classes = (CheckTokenPermission,)

    @method_decorator(request_log(level='DEBUG'))
    def single(self, request, **kwargs):
        """获取单个问卷"""
        try:
            instance = self.get_object()
        except Exception as e:
            ret = response.WJ_NOT_EXISTS
            ret['msg'] = str(e)
            return Response(ret)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """获取所有问卷"""

        obj = models.Wj.objects.filter(status=1).all()
        serializer = self.get_serializer(obj, many=True)

        return Response(serializer.data)


class AnswerView(GenericViewSet):
    """答卷相关接口"""

    serializer_class = serializers.AnswerSerializer
    pagination_class = pagination.MyCursorPagination
    permission_classes = (CheckTokenPermission,)
    queryset = models.Answer.objects

    @method_decorator(request_log(level='DEBUG'))
    def post(self, request):
        """保存答卷"""

        submit_ip = request.data.get('submit_ip', '')
        use_time = request.data['use_time']
        answer_choice = json.dumps(request.data.get('answer_choice', ""))
        answer_text = json.dumps(request.data.get('answer_text', ""), ensure_ascii=False)
        try:
            wj_id = request.data['wj_id']
            wj = models.Wj.objects.get(id=wj_id)
            token = request.data['token']
            submit_user = models.RespondentToken.objects.get(key=token).respondents
        except Exception as e:
            logger.error(str(e))
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
            anwser = s.save(wj=wj, submit_user=submit_user)
            answer_sheet.update(response.ANSWER_SAVE_SUCCESS)
            tasks.async_analysis.delay(anwser.id)
            return Response(answer_sheet)
        else:
            logger.info(s.errors)
            answer_sheet.update(response.ANSWER_SAVE_ERROR)
            return Response(answer_sheet)

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """展示所有答题卡"""

        querset = self.get_queryset()
        serializer = self.get_serializer(querset, many=True)

        return Response(serializer.data)

    @method_decorator(request_log(level='DEBUG'))
    def single(self, request, **kwargs):
        """查询指定答卷"""

        try:
            queryset = self.queryset.get(id=kwargs['pk'])
        except:
            return Response(response.ANSWER_NOT_EXIST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RespondentsView(GenericViewSet, mixins.ListModelMixin):
    """应聘者信息"""

    pagination_class = pagination.MyCursorPagination
    permission_classes = (CheckTokenPermission, )
    serializer_class = serializers.RespondentsSerializer
    queryset = models.Respondents.objects

    def get(self, request):
        """获取所有应聘者信息"""

        respondent = self.get_queryset()
        s = self.get_serializer(respondent, many=True)
        return Response(s.data)

    def single(self, request, **kwargs):
        """获取某个应聘者信息信息"""

        try:
            respondent = self.queryset.filter(id=kwargs['pk'])
        except:
            return Response(response.RESPONDENT_NOT_EXIST)
        s = self.get_serializer(respondent, many=True)
        return Response(s.data)

    def post(self, request, *args, **kwargs):
        """ 保存应聘者信息"""

        ret = BaseResponse()
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token, created = models.RespondentToken.objects.get_or_create(respondents=user)
                ret.msg = "信息保存成功！"
                ser_obj = self.serializer_class(user)
                ret.data = ser_obj.data
                ret.token = token.key
        except Exception as e:
            logger.error(e)
            ret.code = 1013
            ret.msg = str(e)
        return Response(ret.dict)


class PositionView(GenericViewSet, mixins.ListModelMixin):
    pagination_class = pagination.MyCursorPagination
    permission_classes = (CheckTokenPermission,)
    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects