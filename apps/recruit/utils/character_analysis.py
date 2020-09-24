#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from recruit import models
from recruit.utils import response

def get_charater_detail(pk):
    try:
        charater = models.Character.objects.filter(id=pk).values()
    except:
        return response.CHARATER_NOT_EXISTS

    return charater
