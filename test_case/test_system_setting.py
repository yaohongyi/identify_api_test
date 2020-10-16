#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from api.other import create_random_str


class TestSystemSetting:
    def test_add_level_1_case_classify(self, api_object):
        """测试新建一级案件分类"""
        classify_name = create_random_str(8)
        res = api_object.add_level_1_case_classify(classify_name)
        has_error = res.get('hasError')
        if has_error is False:
            classify_id = res.get('data').get('typeId')
            find_result = api_object.find_case_classify_by_id(classify_id)
            assert find_result
            # 环境还原
            api_object.remove_case_classify(classify_id)
        else:
            assert False

    def test_add_level_2_case_classify(self, api_object):
        """测试新增二级案件分类"""
        # 先新增一级案件分类
        level_1_classify_name = create_random_str(8)
        res_1 = api_object.add_level_1_case_classify(level_1_classify_name)
        level_1_classify_id = res_1.get('data').get('typeId')
        # 新增二级案件分类
        level_2_classify_name = create_random_str(8)
        classify_list = [
            {"parentId": level_1_classify_id, "sign": f"name0-{level_2_classify_name}", "name": level_2_classify_name}
        ]
        res_2 = api_object.add_level_2_case_classify(classify_list)
        has_error = res_2.get('hasError')
        if has_error is False:
            find_result = api_object.find_level_2_case_classify(level_2_classify_name, level_1_classify_id)
            assert find_result
        # 直接删除一级案件分类进行环境还原
        api_object.remove_case_classify(level_1_classify_id)

    def test_edit_case_classify(self, api_object):
        """测试编辑案件分类"""
        # 新建一级案件分类
        classify_name = create_random_str(8)
        res = api_object.add_level_1_case_classify(classify_name)
        classify_id = res.get('data').get('typeId')
        # 修改案件分类名称
        new_classify_name = create_random_str(8)
        api_object.edit_case_classify(classify_id, new_classify_name)
        # 断言是否修改成功
        find_result = api_object.find_case_classify_name_by_id(classify_id, new_classify_name)
        assert find_result
        # 环境清理
        api_object.remove_case_classify(classify_id)

    def test_remove_case_classify(self, api_object):
        """测试删除案件分类"""
        # 新建一级案件分类
        classify_name = create_random_str(8)
        res = api_object.add_level_1_case_classify(classify_name)
        classify_id = res.get('data').get('typeId')
        # 删除案件分类
        api_object.remove_case_classify(classify_id)
        # 验证能否找到被删除的案件分类
        find_result = api_object.find_case_classify_by_id(classify_id)
        assert find_result is False
