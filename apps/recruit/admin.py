#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from constance import config
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin

from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    UploadFile, RespondentToken, Position
from recruit.resources import RespondentsResource, WJResource, QuestionResource, OptionsResource, AnswerResource, \
AnimalResource, CharacterResource, AnalysisDataResource, ReportDataResource, PositionDataResource


admin.site.site_header = '瑞云问卷调查后台'
admin.site.site_title = '瑞云问卷调查'


class RespondentTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'create_time', 'respondents', 'status']
    readonly_fields = ['key', 'create_time', 'status', 'respondents']


class RespondentsAdmin(ImportExportActionModelAdmin):
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


class WjAdmin(ImportExportActionModelAdmin):
    list_display = ["title", "wj_alias", "get_questions", "get_questions_qid", "status", "desc", "create_by",
                    'max_quiz_time']
    list_display_link = ["title", "status", "create_by"]
    search_fields = ["title", "status"]
    list_filter = ["title", "status", "create_by", 'create_time', 'update_time']
    ordering = ['id']
    list_editable = ['status', 'max_quiz_time']
    resource_class = WJResource

    def get_questions(self, obj):
        return Question.objects.filter(wjId=obj.id).count()

    get_questions.short_description = "试题总数"
    get_questions.allow_tags = True

    def get_questions_qid(self, obj):
        qu = Question.objects.filter(wjId=obj.id).values('qid')
        return [i['qid'] for i in qu]

    get_questions_qid.short_description = "试题序号"
    get_questions_qid.allow_tags = True


class QuestionAdmin(ImportExportActionModelAdmin):
    list_display = ["qid", "title", "type", "wjId", 'animal', 'get_options', "get_wj_alias", "must", "create_by"]
    list_display_link = ["title", "type", "create_by"]
    search_fields = ["title", "type"]
    list_filter = ["title", "type", "create_by", 'wjId', 'create_time', 'update_time']
    ordering = ['qid']
    list_per_page = 20
    resource_class = QuestionResource

    def get_options(self, obj):
        options = Question.objects.get(id=obj.id).options.values('title')
        return json.dumps([i['title'] for i in options], ensure_ascii=False)

    get_options.short_description = "选项"
    get_options.allow_tags = True

    def get_wj_alias(self, obj):
        return obj.wjId.wj_alias

    get_wj_alias.short_description = "问卷别名"
    get_wj_alias.allow_tags = True


class OptionsAdmin(ImportExportActionModelAdmin):
    list_display = ["title", "score"]
    search_fields = ["title", "score"]
    list_filter = ["title", "score"]
    ordering = ['-update_time']


class AnswerAdmin(ImportExportActionModelAdmin):
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


class AnimalAdmin(ImportExportActionModelAdmin):
    search_fields = ["name", "feature"]
    list_filter = ["name", "id", "wj"]


class CharacterAdmin(ImportExportActionModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]
    list_export = ["json", "xls", "csv"]


class AnalysisDataAdmin(ImportExportActionModelAdmin):
    search_fields = ["name", "content"]
    list_filter = ["name", "tags", "wj"]
    list_export = ["json", "xls", "csv"]
    style_fields = {'tags': 'm2m_transfer'}


class ReportAdmin(ImportExportActionModelAdmin):
    list_display = ['respondenter', 'answer', 'result']


class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'status', 'create_by']
    readonly_fields = ['name', 'status', 'create_by', 'file']


class PositionAdmin(ImportExportActionModelAdmin):
    list_display = ['name']


admin.site.register(Respondents, RespondentsAdmin)
admin.site.register(Wj, WjAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Options, OptionsAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(AnalysisData, AnalysisDataAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(RespondentToken, RespondentTokenAdmin)
admin.site.register(Position, PositionAdmin)
