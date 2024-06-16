# -*- coding:utf8 -*-

import json


def default(self, obj):
    if isinstance(obj, bytes):
        return str(obj, encoding='utf-8')

    return json.JSONEncoder.default(self, obj)