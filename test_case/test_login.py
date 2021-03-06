#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from api.other import read_excel
from api.operate_api import operate_login


class TestLogin:
    @staticmethod
    def test_login_success(api_object):
        """成功登录"""
        excel_data = read_excel('test_login_success')
        username = excel_data.get('username')
        password = excel_data.get('password')
        session_id = api_object.get_session_id(username, password)
        assert session_id

    def test_username_none(self):
        """用户名为空登录"""
        excel_data = read_excel('test_username_none')
        username = excel_data.get('username')
        password = excel_data.get('password')
        msg = excel_data.get('msg')
        res = operate_login(username, password)
        error_desc = res.get('errorDesc')
        assert error_desc == msg

    def test_password_none(self):
        """密码为空登录"""
        excel_data = read_excel('test_password_none')
        username = excel_data.get('username')
        password = excel_data.get('password')
        msg = excel_data.get('msg')
        res = operate_login(username, password)
        error_desc = res.get('errorDesc')
        assert error_desc == msg

    def test_username_password_none(self):
        """用户名、密码为空登录"""
        excel_data = read_excel('test_username_password_none')
        username = excel_data.get('username')
        password = excel_data.get('password')
        msg = excel_data.get('msg')
        res = operate_login(username, password)
        error_desc = res.get('errorDesc')
        assert error_desc == msg

    def test_username_wrong(self):
        """用户名错误登录"""
        excel_data = read_excel('test_username_wrong')
        username = excel_data.get('username')
        password = excel_data.get('password')
        msg = excel_data.get('msg')
        res = operate_login(username, password)
        error_desc = res.get('errorDesc')
        assert error_desc == msg

    def test_password_wrong(self):
        """密码错误登录"""
        excel_data = read_excel('test_password_wrong')
        username = excel_data.get('username')
        password = excel_data.get('password')
        msg = excel_data.get('msg')
        res = operate_login(username, password)
        error_desc = res.get('errorDesc')
        assert error_desc == msg

    def test_change_password(self, api_object):
        """修改当前登录用户的密码"""
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
