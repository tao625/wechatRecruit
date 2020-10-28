#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from constance import config
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin

from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    RespondentToken, Position
from recruit.resources import WJResource, QuestionResource, OptionsResource, AnswerResource, \
    AnimalResource, CharacterResource, AnalysisDataResource, ReportResource, PositionDataResource, \
    RespondentsResource
from recruit.utils.actions import force_analysis

admin.site.site_header = '瑞云调查问卷后台'
admin.site.site_title = '瑞云调查问卷'


# @admin.register(LogEntry)
class CommonSettingAdmin(admin.ModelAdmin):
    list_per_page = 20


class RespondentTokenAdmin(CommonSettingAdmin):
    list_display = ['key', 'create_time', 'respondents', 'status']
    readonly_fields = ['key', 'status']


class RespondentsAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = RespondentsResource
    list_display = [obj.name for obj in Respondents._meta.fields]
    search_fields = ['name', 'email', 'phone', 'intention_position']
    list_filter = ['intention_position']


class WjAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = WJResource
    list_display = [obj.name for obj in Wj._meta.fields]
    search_fields = ['title', 'wj_alias', 'desc']
    list_filter = ['status', 'create_by', 'type', 'max_quiz_time']


class QuestionAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    ordering = ['qid']
    resource_class = QuestionResource
    list_display = [obj.name for obj in Question._meta.fields]
    search_fields = ['title']
    list_filter = ['type', 'wj_name', 'animal_name', 'create_by']
    list_per_page = 20


class OptionsAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = OptionsResource
    list_display = [obj.name for obj in Options._meta.fields]


class AnswerAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    refresh_times = [1, 30, 60, 300]
    resource_class = AnswerResource
    list_display = [obj.name for obj in Answer._meta.fields]
    search_fields = ['submit_ip', 'use_time']
    list_filter = ['wj', 'submit_user']
    date_hierarchy = 'create_time'
    actions = [force_analysis]

    force_analysis.short_description = '手动更新'
    force_analysis.type = 'warning'
    force_analysis.confirm = '确定？一定？以及肯定？'


class AnimalAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = AnimalResource
    list_display = [obj.name for obj in Animal._meta.fields]
    search_fields = ['feature', 'name']
    list_filter = ['name', 'wj']


class CharacterAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = CharacterResource
    list_display = [obj.name for obj in Character._meta.fields]
    search_fields = ['name', 'content', 'wj']
    list_filter = ['animal', 'name', 'wj']


class AnalysisDataAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = AnalysisDataResource
    list_display = [obj.name for obj in AnalysisData._meta.fields]
    search_fields = ['tags', 'wj_name', 'content']
    list_filter = ['tags', 'wj_name', 'name']


class ReportAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = ReportResource
    list_display = [obj.name for obj in Report._meta.fields] + ["analyze"]
    search_fields = ['respondenter_name', 'result']


    def analyze(self, obj):
        url = "{ip}/recruit/report/{id}/".format(ip=config.URL, id=str(obj.id))
        return mark_safe('<a href={url} target="_blank">分析结果</a>'.format(url=url))

    analyze.short_description = "页面展示"
    analyze.allow_tags = '页面展示'


class PositionAdmin(ImportExportActionModelAdmin, CommonSettingAdmin):
    resource_class = PositionDataResource
    list_display = [obj.name for obj in Position._meta.fields]
    skip_admin_log = True


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['object_repr', 'action_flag', 'user', 'change_message', 'action_time']


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
