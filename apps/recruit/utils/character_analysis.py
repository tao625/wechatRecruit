#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
from recruit import models
from recruit.conf import character_2
from constance import config
from . import logger

class AnalyzeCharacter(object):
    """性格分析

    """

    def execute(self, pk):
        type = models.Answer.objects.get(id=pk).wj.type
        if type == 1:
            answer = self.get_answer_1(pk)
            scores = self.get_scores_1(answer)
            character = self.analyze_1(scores)
            logger.info({"pk": pk, "type": 1, "answer": answer, "scores": scores, "character": character})
        elif type == 2:
            scores = self.get_answer_2(pk)
            character = self.analyze_2(scores)
            logger.info({"pk": pk, "type": 2, "scores": scores, "character": character})

        return character, scores

    def analyze_1(self, scores):
        """分析 PDP性格测试

        :return: [()]
        """
        charater = []
        data = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        if data[0][1] - data[1][1] > config.PROMINENT:
            charater = [data[0]]
        elif data[1][1] - data[2][1] > config.COMMON:
            charater = [data[0], data[1]]
        elif data[0][1] - data[-1][1] <= config.BALANCE:
            charater = data

        return dict(charater)

    def analyze_2(self, scores):
        """分析霍兰德职业测试

        :return:
        """

        data = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        if len(data) == 0:
            return dict(data)
        return dict([data[0], data[1], data[2]])


    def get_answer_1(self, pk):
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
            wj_name = wj.title
            animal_name = models.Question.objects.get(qid=int(k), wj_name=wj.title).animal_name
            if animal_name:
                name = animal_name
            else:
                name = "total"
            old = op_ids.get(name)
            if old:
                old.extend(v)
            else:
                op_ids[name] = v

        return op_ids

    def get_answer_2(self, pk):
        op_ids = {}
        answer = models.Answer.objects.get(id=pk)
        answer_choice = json.loads(answer.answer_choice) or {}
        for k, v in answer_choice.items():
            title = models.Options.objects.get(id=v[0]).title
            for name, val in character_2.items():
                count = op_ids.get(name, 0)
                if int(k) in val[title]:
                    count += 1
                    op_ids[name] = count
                    break
                op_ids[name] = count

        return op_ids

    def get_scores_1(self, answer: dict):
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
