#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import os

import pandas as pd
from recruit.models import Question, Wj, User, Animal, Options, UploadFile
from . import logger
from celery import shared_task

def get_type(str1):
    for k, v in dict(Question.q_type).items():
        if v == str1.strip():
            return k

def insert_data(datas):
    for q in datas:
        wj = Wj.objects.get(title=q['wjId'])
        create_by = User.objects.get(username=q['create_by'])
        animal = None if q['animal'] == "空" or not q['animal'] else Animal.objects.get(name=q['animal'])
        type = get_type(q['type'])
        op = json.loads(q['options'].replace('&quot;', '"'))
        options_list = Options.objects.filter(title__in=op)

        q.update(wjId=wj, create_by=create_by, animal=animal, type=type)
        q.pop('options')
        obj, flag = Question.objects.update_or_create(**q)
        obj.options.set(options_list)

@shared_task
def get_data(path, id=None):
    names = ['qid', 'title', 'type', 'wjId', 'animal', 'options', 'must', 'create_by']
    dfs = pd.read_excel(io=path, names=names, sheet_name=None)
    for sheet_name, df in dfs.items():
        df = df.fillna(value="")
        datas = df.to_dict(orient='records')
        logger.info(datas)
        insert_data(datas)
    if os.path.exists(path):
        if id:
            UploadFile.objects.filter(id=id).update(status=2)
            logger.info({"id": id, "message": "文件状态修改成功", "path": path})
        os.remove(path)