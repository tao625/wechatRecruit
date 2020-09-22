#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from rest_framework import serializers
from recruit.models import Wj, Question

class WJSerializer(serializers.ModelSerializer):
    """
    问卷序列化
    """

    class Meta:
        model = Wj
        fields = "__all__"
