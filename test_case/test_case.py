#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from api.operate_api import OperateApi
from api.other import create_case_name, read_excel, create_random_str, get_file_name


class TestCase:
    def test_add_private_case(self, get_api_object):
        """新增私有案件"""
        api_object = get_api_object
        excel_data = read_excel('test_add_private_case')
        private_case = bool(excel_data.get('private_case'))
        # 新增私有案件
        case_name = create_case_name()
        api_object.add_case(case_name, private_case)
        # 查询案件是否新增成功
        find_result = api_object.find_case_in_case_list(case_name)
        assert find_result

    def test_add_share_case(self, get_api_object):
        """新增共享案件"""
        api_object = get_api_object
        excel_data = read_excel('test_add_share_case')
        private_case = bool(excel_data.get('private_case'))
        # 新增共享案件
        case_name = create_case_name()
        api_object.add_case(case_name, private_case)
        # 查询案件是否新增成功
        find_result = api_object.find_case_in_case_list(case_name)
        assert find_result

    def test_rename_case(self, get_api_object):
        """案件重命名"""
        api_object = get_api_object
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 重命名案件
        new_case_name = case_name + '_new'
        api_object.rename_case(new_case_name, case_id)
        # 验证案件是否重命名成功
        find_result = api_object.find_case_in_case_list(new_case_name)
        assert find_result

    def test_remove_case(self, get_api_object):
        """从案件列表删除案件"""
        api_object = get_api_object
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 删除案件
        api_object.remove_case(case_id)
        # 在案件列表查找案件(不存在)
        find_case_list_result = api_object.find_case_in_case_list(case_name)
        assert find_case_list_result is False
        # 在案件回收站查找案件(存在)
        find_recycle_bin_result = api_object.find_case_in_recycle_bin(case_name)
        assert find_recycle_bin_result

    def test_restore_case(self, get_api_object):
        """从案件回收站还原案件"""
        api_object = get_api_object
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 删除案件
        api_object.remove_case(case_id)
        # 还原案件
        api_object.restore_case(case_id)
        # 在案件回收站查找案件(不存在)
        find_recycle_bin_result = api_object.find_case_in_recycle_bin(case_name)
        assert find_recycle_bin_result is False
        # 在案件列表查找案件(存在)
        find_case_list_result = api_object.find_case_in_case_list(case_name)
        assert find_case_list_result

    def test_complete_remove_case(self, get_api_object):
        """从案件回收站彻底删除案件"""
        api_object = get_api_object
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 删除案件
        api_object.remove_case(case_id)
        # 还原案件
        api_object.complete_remove_case(case_id)
        # 在案件回收站查找案件(不存在)
        find_recycle_bin_result = api_object.find_case_in_recycle_bin(case_name)
        assert find_recycle_bin_result is False
        # 在案件列表查找案件(不存在)
        find_case_list_result = api_object.find_case_in_case_list(case_name)
        assert find_case_list_result is False

    def test_sync_my_case(self, get_api_object):
        """测试同步我的案件"""
        api_object = get_api_object
        res = api_object.sync_my_case()
        has_error = res.get('hasError')
        assert has_error is False

    def test_sync_other_case(self, get_api_object):
        """测试同步他人案件"""
        api_object = get_api_object
        res = api_object.sync_other_case()
        has_error = res.get('hasError')
        assert has_error is False

    def test_sync_all_case(self, get_api_object):
        """测试同步所有案件"""
        api_object = get_api_object
        res = api_object.sync_all_case()
        has_error = res.get('hasError')
        assert has_error is False

    def test_add_folder(self, get_api_object):
        """测试新增文件夹"""
        api_object = get_api_object
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 验证案件下是否存在新增的文件夹
        find_result = api_object.find_folder_by_id(case_id, folder_id)
        assert find_result

    def test_upload_voice(self, get_api_object):
        """上传音频"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_upload_voice')
        file_path = excel_data.get('file_path')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 验证文件是否上传成功
        find_result = api_object.find_file_by_id(case_id, folder_id, file_id)
        assert find_result

    def test_remove_voice(self, get_api_object):
        """删除音频"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_remove_voice')
        file_path = excel_data.get('file_path')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 删除音频
        api_object.remove_voice(file_id)
        # 验证音频是否删除成功
        find_result = api_object.find_file_by_id(case_id, folder_id, file_id)
        assert find_result is False

    def test_upload_picture(self, get_api_object):
        """上传图片"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_upload_picture')
        file_path = excel_data.get('file_path')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传图片
        mime_type = 'application/octet-stream'
        file_id = api_object.upload_file_to_folder(case_id, file_path, mime_type, folder_id)
        # 验证文件是否上传成功
        find_result = api_object.find_file_by_id(case_id, folder_id, file_id)
        assert find_result

    def test_remove_picture(self, get_api_object):
        """删除图片"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_remove_picture')
        file_path = excel_data.get('file_path')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传图片
        mime_type = 'application/octet-stream'
        file_id = api_object.upload_file_to_folder(case_id, file_path, mime_type, folder_id)
        # 删除图片
        api_object.remove_attachment(file_id)
        # 验证图片是否删除成功
        find_result = api_object.find_file_by_id(case_id, folder_id, file_id)
        assert find_result is False

    def test_rename_file(self, get_api_object):
        """测试文件重命名"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_upload_picture')
        file_path = excel_data.get('file_path')
        file_name = get_file_name(file_path)
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传图片
        mime_type = 'application/octet-stream'
        file_id = api_object.upload_file_to_folder(case_id, file_path, mime_type, folder_id)
        # 修改文件名称
        new_name = 'new_' + file_name
        api_object.rename_file(file_id, new_name)
        find_result = api_object.find_file_by_name(case_id, folder_id, new_name)
        assert find_result

    def test_case_allocate_user(self, get_api_object):
        """分发案件个单个用户"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_case_allocate_user')
        file_path = excel_data.get('file_path')
        target_user_group = excel_data.get('target_user_group')
        target_username = excel_data.get('target_username')
        target_password = excel_data.get('target_password')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 获取用户id
        user_group_id = api_object.get_auth_group_id_by_name(target_user_group)
        user_id = api_object.get_user_id_by_name(user_group_id, target_username)
        # 将案件转发给他人
        user_ids = list()
        user_ids.append(user_id)
        api_object.case_allocate(case_id, user_ids)
        # 验证用户是否接收到案件
        new_operate_api = OperateApi(target_username, target_password)
        new_operate_api.get_session_id()
        target_case_name = case_name + '_' + target_username
        find_result = new_operate_api.find_case_in_case_list(target_case_name)
        assert find_result

    def test_add_tag(self, get_api_object):
        """测试添加标记"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_add_tag')
        file_path = excel_data.get('file_path')
        begin_time = int(excel_data.get('begin_time'))
        end_time = int(excel_data.get('end_time'))
        tag_name = excel_data.get('tag_name')
        comment = excel_data.get('comment')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 给音频文件添加标记
        tag_id = api_object.add_tag(begin_time, end_time, case_id, tag_name, file_id, comment)
        # 验证标记是否添加成功
        tag_info = api_object.get_tag_info(case_id, file_id, tag_id)
        res_tag_name = tag_info.get('voiceTagName')
        res_tag_comment = tag_info.get('comment')
        res_begin_time = tag_info.get('beginTime')
        res_end_time = tag_info.get('endTime')
        assert (res_tag_name == tag_name and res_tag_comment == comment and res_begin_time == begin_time
                and res_end_time == end_time)

    def test_update_tag(self, get_api_object):
        """测试更新标记"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_update_tag')
        file_path = excel_data.get('file_path')
        begin_time = int(excel_data.get('begin_time'))
        end_time = int(excel_data.get('end_time'))
        tag_name = excel_data.get('tag_name')
        comment = excel_data.get('comment')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 给音频文件添加标记
        tag_id = api_object.add_tag(begin_time, end_time, case_id, tag_name, file_id, comment)
        # 更新标记
        new_begin_time = begin_time - 10
        new_end_time = end_time + 10
        new_comment = comment + '_new'
        new_tag_name = tag_name + '_new'
        api_object.update_tag(new_begin_time, new_end_time, tag_id, new_tag_name, new_comment)
        # 验证标记是否更新成功
        tag_info = api_object.get_tag_info(case_id, file_id, tag_id)
        res_tag_name = tag_info.get('voiceTagName')
        res_tag_comment = tag_info.get('comment')
        res_begin_time = tag_info.get('beginTime')
        res_end_time = tag_info.get('endTime')
        assert (res_tag_name == new_tag_name and res_tag_comment == new_comment and
                res_begin_time == new_begin_time and res_end_time == new_end_time)

    def test_remove_tag(self, get_api_object):
        """测试删除标记"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_remove_tag')
        file_path = excel_data.get('file_path')
        begin_time_1 = int(excel_data.get('begin_time_1'))
        end_time_1 = int(excel_data.get('end_time_1'))
        tag_name_1 = excel_data.get('tag_name_1')
        comment_1 = excel_data.get('comment_1')
        begin_time_2 = int(excel_data.get('begin_time_2'))
        end_time_2 = int(excel_data.get('end_time_2'))
        tag_name_2 = excel_data.get('tag_name_2')
        comment_2 = excel_data.get('comment_2')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 给音频文件添加标记
        tag_id_1 = api_object.add_tag(begin_time_1, end_time_1, case_id, tag_name_1, file_id, comment_1)
        tag_id_2 = api_object.add_tag(begin_time_2, end_time_2, case_id, tag_name_2, file_id, comment_2)
        tag_ids = [tag_id_1, tag_id_2]
        # 删除标记
        api_object.remove_tag(tag_ids)
        # 验证标记列表已经不存在被删除的标记
        find_result_1 = api_object.find_tag_by_id(case_id, file_id, tag_id_1)
        assert find_result_1 is False
        find_result_2 = api_object.find_tag_by_id(case_id, file_id, tag_id_2)
        assert find_result_2 is False
        # 验证回收站存在刚才被删除的标记
        find_result_3 = api_object.find_tag_in_recycle_by_id(case_id, tag_id_1)
        assert find_result_3
        find_result_4 = api_object.find_tag_in_recycle_by_id(case_id, tag_id_2)
        assert find_result_4

    def test_recover_tag(self, get_api_object):
        """回收站还原标记"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_recover_tag')
        file_path = excel_data.get('file_path')
        begin_time_1 = int(excel_data.get('begin_time_1'))
        end_time_1 = int(excel_data.get('end_time_1'))
        tag_name_1 = excel_data.get('tag_name_1')
        comment_1 = excel_data.get('comment_1')
        begin_time_2 = int(excel_data.get('begin_time_2'))
        end_time_2 = int(excel_data.get('end_time_2'))
        tag_name_2 = excel_data.get('tag_name_2')
        comment_2 = excel_data.get('comment_2')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 给音频文件添加标记
        tag_id_1 = api_object.add_tag(begin_time_1, end_time_1, case_id, tag_name_1, file_id, comment_1)
        tag_id_2 = api_object.add_tag(begin_time_2, end_time_2, case_id, tag_name_2, file_id, comment_2)
        tag_ids = [tag_id_1, tag_id_2]
        # 删除标记
        api_object.remove_tag(tag_ids)
        # 还原标记
        api_object.recover_tag(tag_ids)
        # 验证标记已经还原到标记列表
        find_result_1 = api_object.find_tag_by_id(case_id, file_id, tag_id_1)
        assert find_result_1
        find_result_2 = api_object.find_tag_by_id(case_id, file_id, tag_id_2)
        assert find_result_2
        # 验证回收站不存在被还原的标记
        find_result_3 = api_object.find_tag_in_recycle_by_id(case_id, tag_id_1)
        assert find_result_3 is False
        find_result_4 = api_object.find_tag_in_recycle_by_id(case_id, tag_id_2)
        assert find_result_4 is False

    def test_complete_remove_tag(self, get_api_object):
        """回收站彻底删除标记"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_complete_remove_tag')
        file_path = excel_data.get('file_path')
        begin_time_1 = int(excel_data.get('begin_time_1'))
        end_time_1 = int(excel_data.get('end_time_1'))
        tag_name_1 = excel_data.get('tag_name_1')
        comment_1 = excel_data.get('comment_1')
        begin_time_2 = int(excel_data.get('begin_time_2'))
        end_time_2 = int(excel_data.get('end_time_2'))
        tag_name_2 = excel_data.get('tag_name_2')
        comment_2 = excel_data.get('comment_2')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        file_id = api_object.upload_file_to_folder(case_id, file_path, folder_id=folder_id)
        # 给音频文件添加标记
        tag_id_1 = api_object.add_tag(begin_time_1, end_time_1, case_id, tag_name_1, file_id, comment_1)
        tag_id_2 = api_object.add_tag(begin_time_2, end_time_2, case_id, tag_name_2, file_id, comment_2)
        tag_ids = [tag_id_1, tag_id_2]
        # 删除标记
        api_object.remove_tag(tag_ids)
        # 回收站彻底删除标记
        api_object.remove_tag(tag_ids, optional=2)
        # 验证回收站存在刚才被删除的标记
        find_result_3 = api_object.find_tag_in_recycle_by_id(case_id, tag_id_1)
        assert find_result_3 is False
        find_result_4 = api_object.find_tag_in_recycle_by_id(case_id, tag_id_2)
        assert find_result_4 is False

    def test_add_hearing_analysis(self, get_api_object):
        """测试新增听觉量化分析记录"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_add_hearing_analysis')
        file_path_1 = excel_data.get('file_path_1')
        file_path_2 = excel_data.get('file_path_2')
        recode_state = bool(excel_data.get('recode_state'))
        pitch_level_score = int(excel_data.get('pitch_level_score'))
        pitch_level_comment = excel_data.get('pitch_level_comment')
        pitch_variation_range_score = int(excel_data.get('pitch_variation_range_score'))
        pitch_variation_range_comment = excel_data.get('pitch_variation_range_comment')
        pitch_model_score = int(excel_data.get('pitch_model_score'))
        pitch_model_comment = excel_data.get('pitch_model_comment')
        throat_allover_score = int(excel_data.get('throat_allover_score'))
        throat_allover_comment = excel_data.get('throat_allover_comment')
        throat_bubble_score = int(excel_data.get('throat_bubble_score'))
        throat_bubble_comment = excel_data.get('throat_bubble_comment')
        throat_other_score = int(excel_data.get('throat_other_score'))
        throat_other_comment = excel_data.get('throat_other_comment')
        tone_intensity_score = int(excel_data.get('tone_intensity_score'))
        tone_intensity_comment = excel_data.get('tone_intensity_comment')
        dialect_area_score = int(excel_data.get('dialect_area_score'))
        dialect_area_comment = excel_data.get('dialect_area_comment')
        dialect_foreign_language_score = int(excel_data.get('dialect_foreign_language_score'))
        dialect_foreign_language_comment = excel_data.get('dialect_foreign_language_comment')
        dialect_idiom_score = int(excel_data.get('dialect_idiom_score'))
        dialect_idiom_comment = excel_data.get('dialect_idiom_comment')
        tuning_vowel_score = int(excel_data.get('tuning_vowel_score'))
        tuning_vowel_comment = excel_data.get('tuning_vowel_comment')
        tuning_consonant_score = int(excel_data.get('tuning_consonant_score'))
        tuning_consonant_comment = excel_data.get('tuning_consonant_comment')
        tuning_mispronunciation_score = int(excel_data.get('tuning_mispronunciation_score'))
        tuning_mispronunciation_comment = excel_data.get('tuning_mispronunciation_comment')
        tuning_nasal_score = int(excel_data.get('tuning_nasal_score'))
        tuning_nasal_comment = excel_data.get('tuning_nasal_comment')
        rhythm_speaking_rate_score = int(excel_data.get('rhythm_speaking_rate_score'))
        rhythm_speaking_rate_comment = excel_data.get('rhythm_speaking_rate_comment')
        rhythm_speech_burst_score = int(excel_data.get('rhythm_speech_burst_score'))
        rhythm_speech_burst_comment = excel_data.get('rhythm_speech_burst_comment')
        rhythm_other_score = int(excel_data.get('rhythm_other_score'))
        rhythm_other_comment = excel_data.get('rhythm_other_comment')
        other_incoherence_score = int(excel_data.get('other_incoherence_score'))
        other_incoherence_comment = excel_data.get('other_incoherence_comment')
        other_language_barrier_score = int(excel_data.get('other_language_barrier_score'))
        other_language_barrier_comment = excel_data.get('other_language_barrier_comment')
        other_feature_score = int(excel_data.get('other_feature_score'))
        other_feature_comment = excel_data.get('other_feature_comment')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        material_file_id = api_object.upload_file_to_folder(case_id, file_path_1, folder_id=folder_id)
        sample_file_id = api_object.upload_file_to_folder(case_id, file_path_2, folder_id=folder_id)
        # 新增听觉量化分析记录
        hearing_id = api_object.add_hearing_analysis(material_file_id, sample_file_id, case_id,
                                                     recode_state,
                                                     pitch_level_score, pitch_level_comment,
                                                     pitch_variation_range_score, pitch_variation_range_comment,
                                                     pitch_model_score, pitch_model_comment,
                                                     throat_allover_score, throat_allover_comment,
                                                     throat_bubble_score, throat_bubble_comment,
                                                     throat_other_score, throat_other_comment,
                                                     tone_intensity_score, tone_intensity_comment,
                                                     dialect_area_score, dialect_area_comment,
                                                     dialect_foreign_language_score, dialect_foreign_language_comment,
                                                     dialect_idiom_score, dialect_idiom_comment,
                                                     tuning_vowel_score, tuning_vowel_comment,
                                                     tuning_consonant_score, tuning_consonant_comment,
                                                     tuning_mispronunciation_score, tuning_mispronunciation_comment,
                                                     tuning_nasal_score, tuning_nasal_comment,
                                                     rhythm_speaking_rate_score, rhythm_speaking_rate_comment,
                                                     rhythm_speech_burst_score, rhythm_speech_burst_comment,
                                                     rhythm_other_score, rhythm_other_comment,
                                                     other_incoherence_score, other_incoherence_comment,
                                                     other_language_barrier_score, other_language_barrier_comment,
                                                     other_feature_score, other_feature_comment)
        find_result = api_object.find_hearing_analysis_by_id(case_id, hearing_id)
        assert find_result

    def test_del_hearing_analysis(self, get_api_object):
        """测试删除听觉量化分析记录"""
        api_object = get_api_object
        # 从excel读取数据
        excel_data = read_excel('test_del_hearing_analysis')
        file_path_1 = excel_data.get('file_path_1')
        file_path_2 = excel_data.get('file_path_2')
        recode_state = bool(excel_data.get('recode_state'))
        pitch_level_score = int(excel_data.get('pitch_level_score'))
        pitch_level_comment = excel_data.get('pitch_level_comment')
        pitch_variation_range_score = int(excel_data.get('pitch_variation_range_score'))
        pitch_variation_range_comment = excel_data.get('pitch_variation_range_comment')
        pitch_model_score = int(excel_data.get('pitch_model_score'))
        pitch_model_comment = excel_data.get('pitch_model_comment')
        throat_allover_score = int(excel_data.get('throat_allover_score'))
        throat_allover_comment = excel_data.get('throat_allover_comment')
        throat_bubble_score = int(excel_data.get('throat_bubble_score'))
        throat_bubble_comment = excel_data.get('throat_bubble_comment')
        throat_other_score = int(excel_data.get('throat_other_score'))
        throat_other_comment = excel_data.get('throat_other_comment')
        tone_intensity_score = int(excel_data.get('tone_intensity_score'))
        tone_intensity_comment = excel_data.get('tone_intensity_comment')
        dialect_area_score = int(excel_data.get('dialect_area_score'))
        dialect_area_comment = excel_data.get('dialect_area_comment')
        dialect_foreign_language_score = int(excel_data.get('dialect_foreign_language_score'))
        dialect_foreign_language_comment = excel_data.get('dialect_foreign_language_comment')
        dialect_idiom_score = int(excel_data.get('dialect_idiom_score'))
        dialect_idiom_comment = excel_data.get('dialect_idiom_comment')
        tuning_vowel_score = int(excel_data.get('tuning_vowel_score'))
        tuning_vowel_comment = excel_data.get('tuning_vowel_comment')
        tuning_consonant_score = int(excel_data.get('tuning_consonant_score'))
        tuning_consonant_comment = excel_data.get('tuning_consonant_comment')
        tuning_mispronunciation_score = int(excel_data.get('tuning_mispronunciation_score'))
        tuning_mispronunciation_comment = excel_data.get('tuning_mispronunciation_comment')
        tuning_nasal_score = int(excel_data.get('tuning_nasal_score'))
        tuning_nasal_comment = excel_data.get('tuning_nasal_comment')
        rhythm_speaking_rate_score = int(excel_data.get('rhythm_speaking_rate_score'))
        rhythm_speaking_rate_comment = excel_data.get('rhythm_speaking_rate_comment')
        rhythm_speech_burst_score = int(excel_data.get('rhythm_speech_burst_score'))
        rhythm_speech_burst_comment = excel_data.get('rhythm_speech_burst_comment')
        rhythm_other_score = int(excel_data.get('rhythm_other_score'))
        rhythm_other_comment = excel_data.get('rhythm_other_comment')
        other_incoherence_score = int(excel_data.get('other_incoherence_score'))
        other_incoherence_comment = excel_data.get('other_incoherence_comment')
        other_language_barrier_score = int(excel_data.get('other_language_barrier_score'))
        other_language_barrier_comment = excel_data.get('other_language_barrier_comment')
        other_feature_score = int(excel_data.get('other_feature_score'))
        other_feature_comment = excel_data.get('other_feature_comment')
        # 新建案件
        case_name = create_case_name()
        case_id = api_object.add_case(case_name)
        # 在案件下新建文件夹
        folder_name = create_random_str()
        folder_id = api_object.add_folder(case_id, folder_name)
        # 在文件夹下上传音频
        material_file_id = api_object.upload_file_to_folder(case_id, file_path_1, folder_id=folder_id)
        sample_file_id = api_object.upload_file_to_folder(case_id, file_path_2, folder_id=folder_id)
        # 新增听觉量化分析记录
        hearing_id = api_object.add_hearing_analysis(material_file_id, sample_file_id, case_id,
                                                     recode_state,
                                                     pitch_level_score, pitch_level_comment,
                                                     pitch_variation_range_score, pitch_variation_range_comment,
                                                     pitch_model_score, pitch_model_comment,
                                                     throat_allover_score, throat_allover_comment,
                                                     throat_bubble_score, throat_bubble_comment,
                                                     throat_other_score, throat_other_comment,
                                                     tone_intensity_score, tone_intensity_comment,
                                                     dialect_area_score, dialect_area_comment,
                                                     dialect_foreign_language_score, dialect_foreign_language_comment,
                                                     dialect_idiom_score, dialect_idiom_comment,
                                                     tuning_vowel_score, tuning_vowel_comment,
                                                     tuning_consonant_score, tuning_consonant_comment,
                                                     tuning_mispronunciation_score, tuning_mispronunciation_comment,
                                                     tuning_nasal_score, tuning_nasal_comment,
                                                     rhythm_speaking_rate_score, rhythm_speaking_rate_comment,
                                                     rhythm_speech_burst_score, rhythm_speech_burst_comment,
                                                     rhythm_other_score, rhythm_other_comment,
                                                     other_incoherence_score, other_incoherence_comment,
                                                     other_language_barrier_score, other_language_barrier_comment,
                                                     other_feature_score, other_feature_comment)
        # 将听觉量化分析记录删除
        api_object.del_hearing_analysis(case_id, material_file_id, sample_file_id)
        # 验证记录是否成功删除
        find_result = api_object.find_hearing_analysis_by_id(case_id, hearing_id)
        assert find_result is False
