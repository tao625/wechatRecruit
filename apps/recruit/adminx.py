#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import xadmin
from xadmin import views
from djcelery.models import (
    TaskState, WorkerState,
    PeriodicTask, IntervalSchedule, CrontabSchedule,
)
from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData
from django.utils.safestring import mark_safe


class GlobalSettings(object):
    site_title = "瑞云招聘小助手后台管理系统"
    site_footer = "recruit"


class RespondentsAdmin(object):
    list_display = ["name", "email", "phone", "intention_position"]
    list_display_link = ["name"]
    search_fields = ["name", "email", "phone", "intention_position"]
    list_filter = ['name', 'intention_position', 'create_time', 'update_time']
    ordering = ['-update_time']


class WjAdmin(object):
    list_display = ["id", "title", "get_questions", "get_questions_qid", "status", "desc", "create_by"]
    list_display_link = ["title", "status", "create_by"]
    search_fields = ["title", "status", "create_by"]
    list_filter = ["title", "status", "create_by", 'create_time', 'update_time']
    ordering = ['id']

    def get_questions(self, obj):
        return Question.objects.filter(wjId=obj.id).count()

    get_questions.short_description = "试题总数"
    get_questions.allow_tags = True

    def get_questions_qid(self, obj):
        qu = Question.objects.filter(wjId=obj.id).values('qid')
        return [i['qid'] for i in qu]

    get_questions_qid.short_description = "试题序号"
    get_questions_qid.allow_tags = True

class QuestionAdmin(object):
    list_display = ["qid", "title", "type", "wjId", 'belong_animal', 'get_options', "must", "create_by"]
    list_display_link = ["title", "type", "create_by"]
    search_fields = ["title", "type", "create_by"]
    list_filter = ["title", "type", "create_by", 'wjId', 'create_time', 'update_time']
    ordering = ['qid']

    def get_options(self, obj):
        options = Question.objects.get(id=obj.id).options.values('title')
        return [i['title'] for i in options]

    get_options.short_description = "选项"
    get_options.allow_tags = True

    def belong_animal(self, obj):
        name = obj.animal
        return name

    belong_animal.short_description = "代表动物"
    belong_animal.allow_tags = True


class OptionsAdmin(object):
    list_display = ["title", "score"]
    list_display_link = ["title"]
    search_fields = ["title", "score"]
    list_filter = ["title", "score"]
    ordering = ['-update_time']


class AnswerAdmin(object):
    list_display = ['id', "wj", "submit_user", "use_time", "answer_choice", "answer_text", "analyze"]
    list_display_link = ["wj", "submit_user"]
    search_fields = ["wj", "submit_ip"]
    list_filter = ["wj", "submit_ip", "submit_user"]
    ordering = ['-update_time']

    # def results_analysis(self, obj):
    #     # op_ids = get_answer_choices(obj.id)
    #     # result = get_scores(op_ids)
    #     obj = AnalyzeCharacter(obj.id)
    #     result = obj.execute(type=1, pk=26)
    #     return result
    #
    # results_analysis.short_description = "得分"
    # results_analysis.allow_tags = True

    def analyze(self, obj):
        url = "http://172.16.4.110:8000/recruit/report/{id}/".format(id=str(obj.id))
        return mark_safe('<a href={url}>分析结果</a>'.format(url=url))


class AnimalAdmin(object):
    list_display = ["name", "wj"]
    list_display_link = ["name", "wj"]
    search_fields = ["name", "wj"]
    list_filter = ["name", "id", "wj"]


class CharacterAdmin(object):
    list_display = ["name", "animal", "content", "professional", "wj"]
    list_display_link = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]


class AnalysisDataAdmin(object):
    list_display = ["name", "tags", "content", "wj"]
    list_display_link = ["name", "tags", "wj"]
    search_fields = ["name", "tags", "wj"]
    list_filter = ["name", "tags", "wj"]


# 定时任务表
xadmin.site.register(IntervalSchedule)  # 存储循环任务设置的时间
xadmin.site.register(CrontabSchedule)  # 存储定时任务设置的时间
xadmin.site.register(PeriodicTask)  # 存储任务
xadmin.site.register(TaskState)  # 存储任务执行状态
xadmin.site.register(WorkerState)  # 存储执行任务的worker

# 自定义表
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Respondents, RespondentsAdmin)
xadmin.site.register(Wj, WjAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Options, OptionsAdmin)
xadmin.site.register(Answer, AnswerAdmin)
xadmin.site.register(Animal, AnimalAdmin)
xadmin.site.register(Character, CharacterAdmin)
xadmin.site.register(AnalysisData, AnalysisDataAdmin)
