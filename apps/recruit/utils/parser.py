#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
from recruit import models
from random import Random

def format_json(value):
    try:
        return json.dumps(value, indent=4, ensure_ascii=False, separators=(',', ':'))
    except:
        return value


def get_question_detail(pk):
    """
    获取题目详情
    :return:
    """
    new_question = []
    questions = models.Question.objects.filter(wjId=pk).values("id", "title", "type", "must")
    for q in questions:
        options = models.Options.objects.filter(question__id=q['id']).values("id", "title")
        q.update(options=list(options))
        new_question.append(q)

    return new_question

def get_token():
    length_r = 32
    token = ''
    random = Random()
    for i in range(length_r):
        token += random.choice("abcdefghihijklmnopqrstuvwxyz123456789")
    return token