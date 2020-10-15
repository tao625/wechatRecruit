#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import json
import logging
import random
import traceback
from celery import shared_task

from recruit.utils.character_analysis import AnalyzeCharacter
from recruit import models

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
    result = obj.execute(pk=answer_id)
    try:
        answer = models.Answer.objects.get(id=answer_id)
    except Exception as e:
        traceback.print_exc()

    analyze_data = models.AnalysisData.objects.filter(wj=answer.wj.id).values('content', 'tags')
    contrast = {}
    for per in analyze_data:
        animal_id = per['tags']
        content = per['content']
        name = models.Animal.objects.get(id=animal_id).name
        val = contrast.get(content)
        if val:
            val.append(name)
        else:
            contrast[content] = [name]

    for c, t in contrast.items():
        if set(t) == set(result.keys()):
            anaylze_result['job'] = c
        else:
            anaylze_result['job'] = "无符合的职业推荐"

    data = {}
    for k in result.keys():
        feature = models.Animal.objects.get(name=k, wj=answer.wj.id).feature
        num = str(random.randint(1, 3))
        data[k] = [feature, num]

    anaylze_result['features'] = data if bool(result) else {'无': ['无符合的性格推荐', "0"]}

    flag = models.Report.objects.update_or_create(
        respondenter=answer.submit_user,
        answer=answer,
        defaults={"result": json.dumps(anaylze_result, ensure_ascii=False)}
    )
    logger.info(anaylze_result)
    logger.info("分析结果完成.....")
