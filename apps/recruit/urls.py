#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.urls import path
from recruit.views import api, analyze, files
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path(r'wj/', api.WjView.as_view({
        "get": "list"
    })),

    path(r'wj/<int:pk>/', api.WjView.as_view({
        "get": "single",
    })),

    path(r'answer/', api.AnswerView.as_view({
        'post': 'post',
        'get': 'list'
    })),

    path(r'answer/<int:pk>/', api.AnswerView.as_view({
        'get': 'single',
    })),

    path(r'respondentor/', api.RespondentsView.as_view({
        'get': 'list',
        'post': 'post'
    })),

    path(r'report/<int:pk>/', analyze.AnalysisCharacterView.as_view({
        'get': 'get',
        'post': 'post'
    })),

    path(r'file/', files.FileView.as_view({
        'post': 'create',
        'get': 'get',
    })),

    path(r'docs/', include_docs_urls(title='接口文档'))

]
