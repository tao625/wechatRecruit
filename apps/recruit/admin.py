#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    UploadFile, RespondentToken, Position
from recruit.resources import WJResource, QuestionResource, OptionsResource, AnswerResource, \
    AnimalResource, CharacterResource, AnalysisDataResource, ReportDataResource, PositionDataResource, \
    RespondentsResource

admin.site.site_header = '瑞云问卷调查后台'
admin.site.site_title = '瑞云问卷调查'


class RespondentTokenAdmin(admin.ModelAdmin):
    list_display = ['key', 'create_time', 'respondents', 'status']
    readonly_fields = ['key', 'status']


class RespondentsAdmin(ImportExportActionModelAdmin):
    resource_class = RespondentsResource


class WjAdmin(ImportExportActionModelAdmin):
    resource_class = WJResource


class QuestionAdmin(ImportExportActionModelAdmin):
    ordering = ['qid']
    resource_class = QuestionResource


class OptionsAdmin(ImportExportActionModelAdmin):
    resource_class = OptionsResource

class AnswerAdmin(ImportExportActionModelAdmin):
    refresh_times = [1, 30, 60, 300]
    resource_class = AnswerResource


class AnimalAdmin(ImportExportActionModelAdmin):
    resource_class = AnimalResource

class CharacterAdmin(ImportExportActionModelAdmin):
    resource_class = CharacterResource

class AnalysisDataAdmin(ImportExportActionModelAdmin):
    resource_class = AnalysisDataResource

class ReportAdmin(ImportExportActionModelAdmin):
    resource_class = ReportDataResource

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'status', 'create_by']


class PositionAdmin(ImportExportActionModelAdmin):
    resource_class = PositionDataResource


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
