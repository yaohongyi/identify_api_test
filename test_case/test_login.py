#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from api.other import read_excel


class TestLogin:
    @staticmethod
    def test_login_success(get_api_object):
        """成功登录"""
        api_object = get_api_object
        excel_data = read_excel('test_login_success')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id

    def test_username_none(self, get_api_object):
        """用户名为空登录"""
        api_object = get_api_object
        excel_data = read_excel('test_username_none')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id is None

    def test_password_none(self, get_api_object):
        """密码为空登录"""
        api_object = get_api_object
        excel_data = read_excel('test_password_none')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id is None

    def test_username_password_none(self, get_api_object):
        """用户名、密码为空登录"""
        api_object = get_api_object
        excel_data = read_excel('test_username_password_none')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id is None

    def test_username_wrong(self, get_api_object):
        """用户名错误登录"""
        api_object = get_api_object
        excel_data = read_excel('test_username_wrong')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id is None

    def test_password_wrong(self, get_api_object):
        """密码错误登录"""
        api_object = get_api_object
        excel_data = read_excel('test_password_wrong')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id is None

    def test_change_password(self, get_api_object):
        """修改当前登录用户的密码"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_change_password')
        username = excel_data.get('username')
        password = excel_data.get('password')
        new_password = excel_data.get('new_password')
        # 修改密码
        user_id = api_object.get_user_id(username, password)
        api_object.change_password(user_id, password, new_password)
        # 验证新密码能否登录系统
        session_id = api_object.get_session_id(username, new_password)
        assert session_id
        # 将密码进行还原
        api_object.reset_password(user_id)
