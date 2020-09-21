#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import xadmin
from xadmin import views
from recruit.models import Respondents, Wj, Question, Options, Submit, Answer


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
    list_display = ["title", "status", "desc", "create_by"]
    list_display_link = ["title", "status", "create_by"]
    search_fields = ["title", "status", "create_by"]
    list_filter = ["title", "status", "create_by", 'create_time', 'update_time']
    ordering = ['-update_time']


class QuestionAdmin(object):
    list_display = ["title", "type", "wjId", "must", "create_by"]
    list_display_link = ["title", "type", "create_by"]
    search_fields = ["title", "type", "create_by"]
    list_filter = ["title", "type", "create_by", 'create_time', 'update_time']
    ordering = ['-update_time']


class OptionsAdmin(object):
    list_display = ["questionId", "title"]
    list_display_link = ["title"]
    search_fields = ["title"]
    list_filter = ["title", "questionId"]
    ordering = ['-update_time']


class SubmitAdmin(object):
    list_display = ["wjId", "submitIp", "submitUser", "useTime"]
    list_display_link = ["wjId", "submitUser"]
    search_fields = ["wjId", "submitIp", "submitUser", "useTime"]
    list_filter = ["wjId", "submitIp", "submitUser", "useTime"]
    ordering = ['-update_time']


class AnswerAdmin(object):
    list_display = ["questionId", "submitId", "wjId", "type", "answer", "answerText"]
    list_display_link = ["submitId", "wjId"]
    search_fields = ["submitId", "wjId", "type"]
    list_filter = ["submitId", "wjId", "type"]
    ordering = ['-update_time']


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Respondents, RespondentsAdmin)
xadmin.site.register(Wj, WjAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Options, OptionsAdmin)
xadmin.site.register(Submit, SubmitAdmin)
xadmin.site.register(Answer, AnswerAdmin)