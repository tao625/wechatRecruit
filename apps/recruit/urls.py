#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.urls import path
from recruit.views import api

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
    }))
]
