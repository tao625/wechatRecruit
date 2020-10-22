#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from rest_framework import serializers
from recruit.models import Wj, Question, Options, Answer, Respondents, Character, Report, UploadFile, Position


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
        fields = ['id', 'title', 'wj_alias', 'desc', 'questions', 'max_quiz_time']
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
        extra_kwargs = {
            'name': {
                'help_text': '请填写真实姓名',
                'min_length': 1,
                'max_length': 255,
                'required': True,
                'error_messages': {
                    'min_length': '4个字符',
                    'max_length': '255个字符'
                }
            },
            'email': {
                'help_text': '请输入邮箱',
                'required': True,
            },
            'phone': {
                'help_text': '请输入手机号',
                'required': True,
            },
            'intention_position': {
                'help_text': '请输入应聘职位',
                'min_length': 1,
                'max_length': 255,
                'required': True,
                'error_messages': {
                    'min_length': '4个字符',
                    'max_length': '255个字符'
                }
            }
        }


class AnswerSerializer(serializers.ModelSerializer):
    """
    答题卡序列化
    """
    token = serializers.CharField(help_text='应聘者信息生产的token', required=False)
    wj_id = serializers.CharField(help_text='试卷ID', required=False)
    wj = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'submit_ip', 'use_time', 'answer_choice', 'answer_text', 'submit_user', 'wj', 'token', 'wj_id']
        depth = 1
        extra_kwargs = {
            'token': {
                'help_text': '应聘者基本信息生产的Token值,非登陆用户token',
                'required': True
            },
            'submit_ip': {
                'help_text': '请输入邮箱',
                'required': True
            },
            'use_time': {
                'help_text': '答题耗时',
                'required': True,
            },
            'wj_id': {
                'help_text': '试卷ID',
                'required': True
            },
            'answer_choice': {
                'help_text': '选择题答案,字典的形式 {"题号":[答案ID]}',
            },
            'answer_text': {
                'help_text': '主观题答案,字典的形式 {"题号": "答案"}',
            }
        }


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

class FileSerializer(serializers.ModelSerializer):
    """
    文件信息序列化
    """
    file = serializers.FileField(required=True, write_only=True, allow_empty_file=False, use_url='excel_data', label="文件",
                                 help_text="文件", error_messages={"blank": "请上传文件", "required": "请上传文件"})

    class Meta:
        model = UploadFile
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    """
    职位
    """

    class Meta:
        model = Position
        fields = ['name']