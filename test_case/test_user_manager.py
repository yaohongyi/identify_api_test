#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from api.other import read_excel


class TestUser:
    def test_add_auth_group(self, api_object, add_auth_group):
        """测试添加用户权限组"""
        group_name, group_id = add_auth_group
        # 验证权限组是否添加成功
        find_result = api_object.find_auth_group_by_name(group_name)
        assert find_result

    def test_update_auth_group_name(self, api_object, add_auth_group):
        """测试修改权限组名称"""
        group_name, group_id = add_auth_group
        # 修改权限组名称
        new_group_name = group_name + "_new"
        api_object.update_name_auth_group(group_id, new_group_name)
        # 验证权限组名称是否修改成功
        find_result = api_object.find_auth_group_by_name(new_group_name)
        assert find_result
        # 删除权限组
        api_object.del_auth_group(group_id)

    def test_del_auth_group(self, api_object, add_auth_group):
        """测试删除权限组"""
        group_name, group_id = add_auth_group
        # 删除权限组
        api_object.del_auth_group(group_id)
        # 验证权限组是否删除成功
        find_result = api_object.find_auth_group_by_name(group_name)
        assert find_result is False

    def test_update_auth_group(self, api_object, add_auth_group):
        """测试修改权限组权限"""
        group_name, group_id = add_auth_group
        # 从excel读取权限数据
        data = read_excel('test_update_auth_group')
        allocate_case_auth = bool(data.get('allocate_case_auth'))
        create_case_auth = bool(data.get('create_case_auth'))
        delete_case_auth = bool(data.get('delete_case_auth'))
        edit_case_auth = bool(data.get('edit_case_auth'))
        give_case_auth = bool(data.get('give_case_auth'))
        manage_user_auth = bool(data.get('manage_user_auth'))
        over_case_auth = bool(data.get('over_case_auth'))
        share_case_auth = bool(data.get('share_case_auth'))
        # 修改用户组权限
        api_object.update_auth_group(group_id, allocate_case_auth, create_case_auth, delete_case_auth, give_case_auth,
                                     manage_user_auth, over_case_auth, share_case_auth)
        # 验证权限是否正确
        auth_list = api_object.get_group_auth(group_id)
        assert allocate_case_auth == auth_list.get('AuthAllocateCase')
        assert create_case_auth == auth_list.get('AuthCreateCase')
        assert delete_case_auth == auth_list.get('AuthDeleteCase')
        assert edit_case_auth == auth_list.get('AuthEditCase')
        assert give_case_auth == auth_list.get('AuthGiveCase')
        assert manage_user_auth == auth_list.get('AuthManageUser')
        assert over_case_auth == auth_list.get('AuthOverCase')
        assert share_case_auth == auth_list.get('AuthShareCase')

    def test_add_user(self, api_object, add_user):
        """测试新增用户"""
        # 新增用户
        group_name, group_id, user_id, user_name = add_user
        # 验证用户是否新增成功
        find_result = api_object.find_user_by_name(group_id, user_name)
        assert find_result

    def test_update_user(self, api_object, add_user):
        """测试编辑用户"""
        # 新增用户
        group_name, group_id, user_id, user_name = add_user
        # 编辑用户
        new_user_name = user_name + '_new'
        api_object.update_user(group_id, user_id, new_user_name)
        # 验证用户是否编辑成功
        find_result = api_object.find_user_by_name(group_id, new_user_name)
        assert find_result
