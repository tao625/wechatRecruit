#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import xadmin
from xadmin import views
from recruit.models import Respondents, Wj, Question, Options, Answer


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
    list_display = ["questionId", "title", "score"]
    list_display_link = ["title"]
    search_fields = ["title", "score"]
    list_filter = ["title", "questionId", "score"]
    ordering = ['-update_time']


class AnswerAdmin(object):
    list_display = ["wj", "submitUser", "useTime", "answerChoice", "answerText"]
    list_display_link = ["wj", "submitUser"]
    search_fields = ["wj", "submitIp"]
    list_filter = ["wj", "submitIp", "submitUser"]
    ordering = ['-update_time']


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Respondents, RespondentsAdmin)
xadmin.site.register(Wj, WjAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Options, OptionsAdmin)
xadmin.site.register(Answer, AnswerAdmin)