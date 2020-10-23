#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import xadmin
from xadmin import views
from constance import config
from django.utils.safestring import mark_safe
from constance.backends.database.models import Constance
from djcelery.models import TaskState, WorkerState, PeriodicTask, IntervalSchedule, CrontabSchedule
from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    UploadFile, RespondentToken, Position
from recruit.resource import RespondentTokenResource, AnalysisDataResource


class GlobalSettings(object):
    site_title = "瑞云招聘小助手后台管理系统"
    site_footer = "recruit"


class BaseSettings(object):
    enable_themes = True  # 使用主题功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSettings)


# 模型注册类
class RespondentTokenAdmin(object):
    list_display = ['key', 'create_time', 'respondents', 'status']
    readonly_fields = ['key', 'create_time', 'status', 'respondents']
    import_export_args = {'import_resource_class': RespondentTokenResource,
                          'export_resource_class': RespondentTokenResource}


class RespondentsAdmin(object):
    list_display = ["name", "email", "phone", "intention_position", 'get_token']
    list_display_link = ["name"]
    search_fields = ["name", "email", "phone", "intention_position"]
    list_filter = ['name', 'intention_position', 'create_time', 'update_time']
    ordering = ['-update_time']

    def get_token(self, obj):
        key = RespondentToken.objects.get(respondents_id=obj).key
        return key


    get_token.short_description = "Token"
    get_token.allow_tags = True


class WjAdmin(object):
    list_display = ["title", "wj_alias", "get_questions", "get_questions_qid", "status", "desc", "create_by", 'max_quiz_time']
    list_display_link = ["title", "status", "create_by"]
    search_fields = ["title", "status"]
    list_filter = ["title", "status", "create_by", 'create_time', 'update_time']
    ordering = ['id']
    list_editable = ['status', 'max_quiz_time']


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
    list_display = ["qid", "title", "type", "wjId", 'animal', 'get_options', "get_wj_alias", "must", "create_by"]
    list_display_link = ["title", "type", "create_by"]
    search_fields = ["title", "type"]
    list_filter = ["title", "type", "create_by", 'wjId', 'create_time', 'update_time']
    ordering = ['qid']
    list_editable = ["title", "type", "wjId", 'animal', 'get_options', "must", "create_by"]
    list_per_page = 20

    def get_options(self, obj):
        options = Question.objects.get(id=obj.id).options.values('title')
        return json.dumps([i['title'] for i in options], ensure_ascii=False)

    get_options.short_description = "选项"
    get_options.allow_tags = True

    def get_wj_alias(self, obj):
        return obj.wjId.wj_alias

    get_wj_alias.short_description = "问卷别名"
    get_wj_alias.allow_tags = True


class OptionsAdmin(object):
    list_display = ["title", "score"]
    list_display_link = ["title"]
    search_fields = ["title", "score"]
    list_filter = ["title", "score"]
    ordering = ['-update_time']
    list_editable = ['title', 'score']


class AnswerAdmin(object):
    list_display = ['id', "wj", "submit_user", "use_time", "answer_choice", "answer_text", "analyze"]
    list_display_link = ["wj", "submit_user"]
    search_fields = ["submit_ip", "use_time"]
    list_filter = ["wj", "submit_user"]
    ordering = ['-update_time']
    readonly_fields = ['id', "wj", "submit_user", "use_time", "answer_choice", "answer_text"]
    refresh_times = [1, 30, 60, 300]
    list_export = ["json", "xls", "csv"]

    def analyze(self, obj):
        url = "{ip}/recruit/report/{id}/".format(ip=config.URL, id=str(obj.id))
        return mark_safe('<a href={url}>分析结果</a>'.format(url=url))


class AnimalAdmin(object):
    list_display = ["name", "wj"]
    list_display_link = ["name", "wj"]
    search_fields = ["name", "feature"]
    list_filter = ["name", "id", "wj"]
    list_editable = ['name', 'wj']


class CharacterAdmin(object):
    list_display = ["name", "animal", "content", "professional", "wj"]
    list_display_link = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_editable = ['name', 'animal', 'wj']
    list_export = ["json", "xls", "csv"]


class AnalysisDataAdmin(object):
    list_display = ['id', "name", "tags", "content", "wj"]
    list_display_link = ["name", "tags", "wj"]
    search_fields = ["name", "content"]
    list_filter = ["name", "tags", "wj"]
    list_export = ["json", "xls", "csv"]
    # style_fields = {'tags': 'm2m_transfer'}
    import_export_args = {'import_resource_class': AnalysisDataResource, 'export_resource_class': AnalysisDataResource}
    ordering = ['id']

    def get_wj(self, obj):
        return Wj.objects.all()

class ReportAdmin(object):
    list_display = ['respondenter', 'answer', 'result']

class ConstanceAdmin(object):
    list_display = ['key', 'value']
    list_editable = ['key', 'value']


class UploadFileAdmin(object):
    list_display = ['name', 'file', 'status', 'create_by']
    readonly_fields = ['name', 'status', 'create_by', 'file']

class PositionAdmin(object):
    list_display = ['name']
    list_editable = ['name']

# 定时任务表
# xadmin.site.register(IntervalSchedule)  # 存储循环任务设置的时间
# xadmin.site.register(CrontabSchedule)  # 存储定时任务设置的时间
# xadmin.site.register(PeriodicTask)  # 存储任务
# xadmin.site.register(TaskState)  # 存储任务执行状态
# xadmin.site.register(WorkerState)  # 存储执行任务的worker

# 常量
xadmin.site.register(Constance, ConstanceAdmin)

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
xadmin.site.register(Report, ReportAdmin)
xadmin.site.register(UploadFile, UploadFileAdmin)
xadmin.site.register(RespondentToken, RespondentTokenAdmin)
xadmin.site.register(Position, PositionAdmin)
