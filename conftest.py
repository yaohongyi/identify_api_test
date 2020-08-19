#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import pytest
from api.operate_api import OperateApi
from api.other import get_config

# 默认测试账号、密码
username = get_config('base_info', 'username')
password = get_config('base_info', 'password')


@pytest.fixture(scope='class')
def get_api_object():
    api_object = OperateApi(username, password)
    yield api_object
    api_object.del_test_case()


@pytest.fixture(scope='function')
def add_auth_group(get_api_object):
    """新增用户组，测试结束删除用户组"""
    group_name = get_config('base_info', 'auth_group_name')
    api_object = get_api_object
    api_object.add_auth_group(group_name)
    group_id = api_object.get_auth_group_id_by_name(group_name)
    yield group_name, group_id
    api_object.del_auth_group(group_id)


@pytest.fixture(scope='function')
def add_user(get_api_object, add_auth_group):
    """新增用户组，测试结束删除用户组"""
    api_object = get_api_object
    group_name, group_id = add_auth_group
    auth_user_name = get_config('base_info', 'auth_user_name')
    # 新增用户
    api_object.add_user(group_id, auth_user_name)
    user_id = api_object.get_user_id_by_name(group_id, auth_user_name)
    yield group_name, group_id, user_id, auth_user_name
    # 删除用户
    api_object.del_user(group_id, user_id)


if __name__ == '__main__':
    get_api_object()
