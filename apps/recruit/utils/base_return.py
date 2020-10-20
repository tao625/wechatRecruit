#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class BaseResponse(object):
    def __init__(self):
        self.code = 1000
        self.msg = ""
        self.data = None
        self.token = ""

    @property
    def dict(self):
        return self.__dict__