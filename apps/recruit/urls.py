#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from recruit.views import api
from recruit.models import Wj

urlpatterns = [
    path(r'wj/', api.WjView.as_view({
        "get": "list"
    })),

    path(r'wj/<int:pk>/', api.WjView.as_view({
        "get": "single",
    }))
]
