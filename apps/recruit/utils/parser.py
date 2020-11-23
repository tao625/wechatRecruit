#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import datetime
import json
import time

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


def string2time_stamp(strValue):

    try:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp
    except ValueError as e:
        d = datetime.datetime.strptime(strValue, "%Y-%m-%d %H:%M:%S")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        return timeStamp