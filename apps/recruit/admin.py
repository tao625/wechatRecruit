#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from constance import config
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin

from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    RespondentToken, Position
from recruit.resources import WJResource, QuestionResource, OptionsResource, AnswerResource, \
    AnimalResource, CharacterResource, AnalysisDataResource, ReportResource, PositionDataResource, \
    RespondentsResource
from recruit.utils.actions import force_analysis

admin.site.site_header = '瑞云问卷调查后台'
admin.site.site_title = '瑞云问卷调查'


class RespondentTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'create_time', 'respondents', 'status']
    readonly_fields = ['key', 'status']


class RespondentsAdmin(ImportExportActionModelAdmin):
    resource_class = RespondentsResource
    list_display = [obj.name for obj in Respondents._meta.fields]
    search_fields = ['name', 'email', 'phone', 'intention_position']
    list_filter = ['intention_position']


class WjAdmin(ImportExportActionModelAdmin):
    resource_class = WJResource
    list_display = [obj.name for obj in Wj._meta.fields]
    search_fields = ['title', 'wj_alias', 'desc', 'intention_position']
    list_filter = ['status', 'create_by', 'type', 'max_quiz_time']


class QuestionAdmin(ImportExportActionModelAdmin):
    ordering = ['qid']
    resource_class = QuestionResource
    list_display = [obj.name for obj in Question._meta.fields]
    search_fields = ['type', 'wj_name', 'animal_name', 'create_by']
    list_filter = ['type', 'wj_name', 'animal_name', 'create_by']


class OptionsAdmin(ImportExportActionModelAdmin):
    resource_class = OptionsResource
    list_display = [obj.name for obj in Options._meta.fields]


class AnswerAdmin(ImportExportActionModelAdmin):
    refresh_times = [1, 30, 60, 300]
    resource_class = AnswerResource
    list_display = [obj.name for obj in Answer._meta.fields]
    search_fields = ['wj', 'submit_ip', 'submit_user', 'use_time']
    list_filter = ['wj', 'submit_user']
    date_hierarchy = 'create_time'
    actions = [force_analysis]

    force_analysis.short_description = '手动更新'


class AnimalAdmin(ImportExportActionModelAdmin):
    resource_class = AnimalResource
    list_display = [obj.name for obj in Animal._meta.fields]
    search_fields = ['name', 'wj', 'feature']
    list_filter = ['name', 'wj']


class CharacterAdmin(ImportExportActionModelAdmin):
    resource_class = CharacterResource
    list_display = [obj.name for obj in Character._meta.fields]
    search_fields = ['name', 'content', 'wj']
    list_filter = ['animal', 'name', 'wj']


class AnalysisDataAdmin(ImportExportActionModelAdmin):
    resource_class = AnalysisDataResource
    list_display = [obj.name for obj in AnalysisData._meta.fields]
    search_fields = ['tags', 'wj_name', 'content']
    list_filter = ['tags', 'wj_name', 'name']


class ReportAdmin(ImportExportActionModelAdmin):
    resource_class = ReportResource
    list_display = [obj.name for obj in Report._meta.fields] + ["analyze"]
    search_fields = ['respondenter_name', 'result', 'answer']
    list_filter = ['respondenter_name', 'answer']

    def analyze(self, obj):
        url = "{ip}/recruit/report/{id}/".format(ip=config.URL, id=str(obj.id))
        return mark_safe('<a href={url} target="_blank">分析结果</a>'.format(url=url))

    analyze.short_description = "页面展示"
    analyze.allow_tags = '页面展示'


class PositionAdmin(ImportExportActionModelAdmin):
    resource_class = PositionDataResource
    list_display = [obj.name for obj in Position._meta.fields]


admin.site.register(Respondents, RespondentsAdmin)
admin.site.register(Wj, WjAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Options, OptionsAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(AnalysisData, AnalysisDataAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(RespondentToken, RespondentTokenAdmin)
admin.site.register(Position, PositionAdmin)
