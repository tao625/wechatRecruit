#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import collections

import tablib
from django.apps import apps
from import_export import resources
from django.db import models
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from recruit.models import Respondents, Wj, Question, Options, Answer, Animal, Character, AnalysisData, Report, \
    UploadFile, RespondentToken, Position


class RespondentTokenResource(resources.ModelResource):
    class Meta:
        model = RespondentToken
        import_id_fields = ['key']


class AnalysisDataResource(resources.ModelResource):
    class Meta:
        model = AnalysisData
        import_id_fields = ['id']
        fields = ['id', 'name', 'content']

    # def __init__(self):
    #     super(AnalysisDataResource, self).__init__()
    #
    #     # 获取recruit应用下AnalysisData模型中的所有字段，请根据自己的应用将recruit更改
    #     field_list = apps.get_model('recruit', 'AnalysisData')._meta.fields
    #     self.vname_dict = {}
    #     self.fkey = ['tags', 'wj']
    #     for i in field_list:
    #         # 获取所有字段的verbose_name并存放在字典
    #         self.vname_dict[i.name] = i.verbose_name
    #         if (isinstance(i, models.ForeignObject)):
    #             # 获取所有ForeignKey字段的name存放在列表
    #             self.fkey.append(i.name)

    # def export(self, queryset=None, *args, **kwargs):
    #     self.before_export(queryset, *args, **kwargs)
    #
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #
    #     headers = self.get_export_headers()
    #     data = tablib.Dataset(headers=headers)
    #
    #     # 获取所有外键名称在headers中的位置
    #     fk_index = {}
    #     for fk in self.fkey:
    #         fk_index[fk] = headers.index(fk)
    #
    #     iterable = queryset
    #     for obj in iterable:
    #         # 获取将要导出的源数据，这里export_resource返回的是列表，便于更改。替换到外键的值
    #         res = self.export_resource(obj)
    #         """
    #         这里是关键，将owner的值到User中获取对应的对象，并截取起可读名称username，
    #         这里用的是get，所以在User的模型中username必须是unique
    #         """
    #         for k, v in fk_index.items():
    #             if ',' in res[v]:
    #                 ids = res[v].split(',')
    #             else:
    #                 ids = res[v]
    #             if not bool(ids):
    #                 res[v] = ""
    #             res[v] = ','.join(v.__str__() for v in Animal.objects.filter(id__in=ids).all())
    #         data.append(res)
    #     self.after_export(queryset, data, *args, **kwargs)
    #     return data

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     dict = []
    #     for row in dataset.dict:
    #         tmp = collections.OrderedDict()
    #         objs = Animal.objects.all()
    #         for item in row:
    #             if item == ['tags', 'wj']:
    #                 """
    #                 这里是关键，通过可读名称到User表中找到对应id，并加到导入的数据中去
    #                 """
    #                 tmp[item] = AnalysisData.objects.filter(name__icontains=row[item]).id
    #             else:
    #                 tmp[item] = row[item]
    #         """
    #         这里是关键，将数据进行比对，如果数据相同，就把原先在Book表中的id加到需要导入的数据中去，
    #         这样就不会新增和原先一模一样的数据，类似于create_or_update方法
    #         """
    #         for obj in objs:
    #             if row['name'] == obj.name:
    #                 tmp['id'] = obj.id
    #         dict.append(tmp)
    #     dataset.dict = dict
    #     return dataset