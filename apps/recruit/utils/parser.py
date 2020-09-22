#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json


def format_json(value):
    try:
        return json.dumps(value, indent=4, ensure_ascii=False, separators=(',', ':'))
    except:
        return value
