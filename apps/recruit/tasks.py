#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import logging
import random
import traceback

from celery import shared_task

from recruit import models
from recruit.utils.character_analysis import AnalyzeCharacter

logger = logging.getLogger('recruit')


@shared_task
def async_analysis(pk):
    """异步执行分析结果

    :return:
    """
    logger.info('分析结果开始..................')
    anaylze_result = {}
    answer_id = pk
    obj = AnalyzeCharacter()
    result, scores = obj.execute(pk=answer_id)
    try:
        answer = models.Answer.objects.get(id=answer_id)
    except Exception as e:
        traceback.print_exc()


    analyze = models.AnalysisData.objects.filter(wj_name=answer.wj.title)
    contrast = {}
    if analyze:
        for item in analyze.values('content', 'tags').all():
            contrast[item['content']] = item['tags']

    for c, t in contrast.items():
        if t == ''.join(result.keys()):
            anaylze_result['job'] = c
            break
        else:
            anaylze_result['job'] = "无符合的职业推荐"

    data = {}
    for k in result.keys():
        feature = models.Animal.objects.get(name=k, wj=answer.wj.title).feature
        num = str(random.randint(1, 3))
        data[k] = [feature, num]

    anaylze_result['features'] = data if bool(result) else {'无': ['无符合的性格推荐', "0"]}

    result_format = json.dumps(anaylze_result, ensure_ascii=False)
    _, flag = models.Report.objects.update_or_create(
        respondenter_name=answer.submit_user,
        answer=answer,
        total_scores=json.dumps(scores, ensure_ascii=False),
        defaults={"result": result_format}
    )
    logger.info(anaylze_result)

    if flag:
        logger.info("【分析创建成功】答卷ID:=>%s" % pk)
    else:
        logger.info("【分析更新成功】答卷ID:=>%s" % pk)
    logger.info("分析结果完成.....")

    return flag