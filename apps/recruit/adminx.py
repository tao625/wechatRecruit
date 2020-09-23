#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import xadmin
from xadmin import views
from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character


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
    list_display = ["id", "title", "get_questions", "status", "desc", "create_by"]
    list_display_link = ["title", "status", "create_by"]
    search_fields = ["title", "status", "create_by"]
    list_filter = ["title", "status", "create_by", 'create_time', 'update_time']
    ordering = ['-update_time']

    def get_questions(self, obj):
        return Question.objects.filter(wjId=obj.id).count()

    get_questions.short_description = "试题总数"
    get_questions.allow_tags = True

class QuestionAdmin(object):
    list_display = ["qid", "title", "type", "wjId", "must", "create_by"]
    list_display_link = ["title", "type", "create_by"]
    search_fields = ["title", "type", "create_by"]
    list_filter = ["title", "type", "create_by", 'create_time', 'update_time']
    ordering = ['qid']


class OptionsAdmin(object):
    list_display = ["title", "score"]
    list_display_link = ["title"]
    search_fields = ["title", "score"]
    list_filter = ["title", "score"]
    ordering = ['-update_time']


class AnswerAdmin(object):
    list_display = ["wj", "submitUser", "useTime", "answerChoice", "answerText"]
    list_display_link = ["wj", "submitUser"]
    search_fields = ["wj", "submitIp"]
    list_filter = ["wj", "submitIp", "submitUser"]
    ordering = ['-update_time']


class AnimalAdmin(object):
    list_display = ["name"]
    list_display_link = ["name"]
    search_fields = ["name"]
    list_filter = ["name", "id"]


class CharacterAdmin(object):
    list_display = ["name", "alias", "animal", "content", "professional", "wj"]
    list_display_link = ["name"]
    search_fields = ["name", "alias"]
    list_filter = ["name", "alias"]


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Respondents, RespondentsAdmin)
xadmin.site.register(Wj, WjAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Options, OptionsAdmin)
xadmin.site.register(Answer, AnswerAdmin)
xadmin.site.register(Animal, AnimalAdmin)
xadmin.site.register(Character, CharacterAdmin)
