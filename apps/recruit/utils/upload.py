#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import pandas as pd
from recruit.models import Question, Wj, User, Animal, Options

def get_type(str1):
    for k, v in dict(Question.q_type).items():
        if v == str1.strip():
            return k

def insert_data(datas):
    # names = ['qid', 'title', 'type', 'wjId', 'animal', 'options', 'must', 'create_by']
    # df = pd.read_excel(io=path, names=names).fillna(value="")
    # datas = df.to_dict(orient='records')
    for q in datas:
        print(q)
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

def get_data(path):
    names = ['qid', 'title', 'type', 'wjId', 'animal', 'options', 'must', 'create_by']
    dfs = pd.read_excel(io=path, names=names, sheet_name=None)
    for sheet_name, df in dfs.items():
        df = df.fillna(value="")
        datas = df.to_dict(orient='records')
        insert_data(datas)