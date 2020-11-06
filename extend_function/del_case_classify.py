#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
"""
删除所有的案件分类
"""

from api.operate_api import OperateApi

oa = OperateApi()
case_classify_list = oa.get_case_classify_list()
for case_classify in case_classify_list:
    type_id = case_classify.get('typeId')
    oa.remove_case_classify(type_id)

case_classify_list = oa.get_case_classify_list()
print(case_classify_list)
