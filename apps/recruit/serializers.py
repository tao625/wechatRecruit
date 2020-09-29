#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from rest_framework import serializers
from recruit.models import Wj, Question, Options, Answer, Respondents, Character, Report

class OptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Options
        fields = ['id', 'title']

class QuestionSerializer(serializers.ModelSerializer):

    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['qid', 'title', 'type', 'must', 'options']

    def get_options(self, obj):
        op = Options.objects.filter(question__id=obj.id)
        serializer = OptionsSerializer(op, many=True)
        return serializer.data


class WJSerializer(serializers.ModelSerializer):
    """
    问卷序列化
    """
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Wj
        fields = ['id', 'title', 'desc', 'questions']
        depth = 1

    def get_questions(self, obj):
        qu = Question.objects.filter(wjId=obj.id)
        serializer = QuestionSerializer(qu, many=True)
        return serializer.data


class RespondentsSerializer(serializers.ModelSerializer):
    """
    答题人序列化
    """

    class Meta:
        model = Respondents
        fields = ['id', 'name', 'email', 'phone', 'intention_position']


class AnswerSerializer(serializers.ModelSerializer):
    """
    答题卡序列化
    """
    submit_user = serializers.SerializerMethodField()
    wj = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'submit_ip', 'use_time', 'answer_choice', 'answer_text', 'submit_user', 'wj']
        depth = 1

    def get_submit_user(self, obj):
        user = Respondents.objects.filter(id=obj.submit_user.id)
        serializer = RespondentsSerializer(user, many=True)
        return serializer.data

    def get_wj(self, obj):
        wj_obj = Wj.objects.filter(id=obj.wj.id)
        serializer = WJSerializer(wj_obj, many=True)
        return serializer.data

class CharacterSerializer(serializers.ModelSerializer):
    """
    性格分析序列化
    """

    class Meta:
        model = Character
        fields = '__all__'
        depth = 1


class ReportSerializer(serializers.ModelSerializer):
    """
    最终分析报告
    """

    class Meta:
        model = Report
        fields = '__all__'
        depth = 1