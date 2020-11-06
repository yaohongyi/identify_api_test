#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
"""
新增案件分类
"""
from api.operate_api import OperateApi
from extend_function.field_map_info import field_map_info

oa = OperateApi()


for level_1_classify, level_2_classify_list in field_map_info.items():
    level_1_res = oa.add_level_1_case_classify(level_1_classify)
    level_1_type_id = level_1_res.get('data').get('typeId')
    level_2_classify_list_len = len(level_2_classify_list)
    classify_list = list()
    i = 0
    for level_2_classify in level_2_classify_list:
        classify = {
            "parentId": level_1_type_id,
            "sign": f"name{i}-{level_2_classify}",
            "name": level_2_classify
        }
        i += 1
        classify_list.append(classify)
    oa.add_level_2_case_classify(classify_list)
    # print(classify_list)
