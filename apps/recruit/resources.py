#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from import_export import resources
from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, Position


class BaseTableResource(resources.ModelResource):
    class Meta:
        # 跳过没有任何修改的行
        skip_unchanged = True
        # 不显示被跳过的行
        report_skipped = False
        # 排除字段
        exclude = ('create_time', 'update_time',)


class RespondentsResource(BaseTableResource):
    class Meta:
        model = Respondents


class WJResource(BaseTableResource):
    class Meta:
        model = Wj


class QuestionResource(BaseTableResource):
    class Meta:
        model = Question


class OptionsResource(BaseTableResource):
    class Meta:
        model = Options


class AnswerResource(BaseTableResource):
    class Meta:
        model = Answer


class AnimalResource(BaseTableResource):
    class Meta:
        model = Animal


class CharacterResource(BaseTableResource):
    class Meta:
        model = Character


class AnalysisDataResource(BaseTableResource):
    class Meta:
        model = AnalysisData


class ReportResource(BaseTableResource):
    class Meta:
        model = Report


class PositionDataResource(BaseTableResource):
    class Meta:
        model = Position
