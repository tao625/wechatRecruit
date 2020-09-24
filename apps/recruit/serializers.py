#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from rest_framework import serializers
from recruit.models import Wj, Question, Options, Answer, Respondents

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

    class Meta:
        model = Answer
        fields = '__all__'
        depth = 1

    def get_submit_user(self, obj):
        user = Respondents.objects.filter(id=obj.submitUser.id)
        serializer = RespondentsSerializer(user, many=True)
        return serializer.data