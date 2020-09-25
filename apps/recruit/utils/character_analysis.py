#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
from recruit import models
from recruit.utils import response


def get_charater_detail(pk):
    """
    获取当前试卷的性格分析详情
    :param pk: 性格表ID
    :return:
    """
    try:
        charater = models.Character.objects.filter(id=pk).values()
    except:
        return response.CHARATER_NOT_EXISTS

    return charater


def get_answer_choices(pk):
    """
    获取选择题答案ID
    :param pk: 答卷ID
    :return:
    """
    op_ids = {}
    answer = models.Answer.objects.get(id=pk)
    answer_choice = answer.answer_choice
    wj = answer.wj
    for k, v in json.loads(answer_choice).items():
        animal = models.Question.objects.get(qid=k, wjId=wj).animal
        if animal:
            name = animal.name
        else:
            name = "total"
        old = op_ids.get(name)
        if old:
            old.extend(v)
        else:
            op_ids[name] = v

    return op_ids


def get_scores(answer: dict):
    """
    获取得分
    :param answer:
        带动物:
            {'猫头鹰': [3, 3], '考拉': [4, 4], '孔雀': [5, 7], '变色龙': [6, 2], '老虎': [7, 6]}
        不带动物:
            {'no_animal': [1, 2, 1, 1, 1, 1, 2, 1, 1, 1]}
    :return:
        带动物:
            {'猫头鹰': 10, '考拉': 8, '孔雀': 4, '变色龙': 2, '老虎': 3}
        不带动物:
            {'total': 8}
    """

    result = dict()
    op = models.Options.objects
    for name, ids in answer.items():
        scores = [op.get(id=id).score for id in ids]
        result[name] = sum(scores)
    return result
