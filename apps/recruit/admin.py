#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    UploadFile, RespondentToken, Position
from recruit.resources import WJResource, QuestionResource, OptionsResource, AnswerResource, \
    AnimalResource, CharacterResource, AnalysisDataResource, ReportResource, PositionDataResource, \
    RespondentsResource

admin.site.site_header = '瑞云问卷调查后台'
admin.site.site_title = '瑞云问卷调查'


class RespondentTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'create_time', 'respondents', 'status']
    readonly_fields = ['key', 'status']


class RespondentsAdmin(ImportExportActionModelAdmin):
    resource_class = RespondentsResource
    list_display = [obj.name for obj in Respondents._meta.fields]


class WjAdmin(ImportExportActionModelAdmin):
    resource_class = WJResource
    list_display = [obj.name for obj in Wj._meta.fields]


class QuestionAdmin(ImportExportActionModelAdmin):
    ordering = ['qid']
    resource_class = QuestionResource
    list_display = [obj.name for obj in Question._meta.fields]


class OptionsAdmin(ImportExportActionModelAdmin):
    resource_class = OptionsResource
    list_display = [obj.name for obj in Options._meta.fields]


class AnswerAdmin(ImportExportActionModelAdmin):
    refresh_times = [1, 30, 60, 300]
    resource_class = AnswerResource
    list_display = [obj.name for obj in Answer._meta.fields]


class AnimalAdmin(ImportExportActionModelAdmin):
    resource_class = AnimalResource
    list_display = [obj.name for obj in Animal._meta.fields]


class CharacterAdmin(ImportExportActionModelAdmin):
    resource_class = CharacterResource
    list_display = [obj.name for obj in Character._meta.fields]


class AnalysisDataAdmin(ImportExportActionModelAdmin):
    resource_class = AnalysisDataResource
    list_display = [obj.name for obj in AnalysisData._meta.fields]


class ReportAdmin(ImportExportActionModelAdmin):
    resource_class = ReportResource
    list_display = [obj.name for obj in Report._meta.fields]


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
