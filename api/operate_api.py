#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from api.interface_api import login, IdentifyApi
from api.other import get_config, get_file_name, find_object_from_list


class OperateApi:
    def __init__(self, username: str = 'yaocheng', password: str = '123456'):
        session_id = self.get_session_id(username, password)
        self.identify_api = IdentifyApi(session_id)

    @staticmethod
    def get_session_id(username: str = 'yaocheng', password: str = '123456'):
        """
        登录系统并获取session_id
        :param username: 用户名
        :param password: 密码
        :return: session_id
        """
        res = login(username, password)
        session_id = res.get('data').get('sessionId')
        return session_id

    @staticmethod
    def get_user_id(username: str = 'yaocheng', password: str = '123456'):
        """
        登录系统并获得user_id
        :param username:
        :param password:
        :return: 用户id
        """
        res = login(username, password)
        user_id = res.get('data').get('userid')
        return user_id

    def add_case(self, case_name: str, private_case: bool = True):
        """新建案件"""
        res = self.identify_api.new_criminal_case(case_name, private_case)
        has_error = res.get('hasError')
        case_id = None
        if has_error is False:
            case_id = res.get('data').get('criminalCaseId')
        return case_id

    def rename_case(self, new_case_name: str, case_id: str):
        """重命名案件"""
        res = self.identify_api.rename_criminal_case(new_case_name, case_id)
        return res

    def find_case_in_case_list(self, keyword: str):
        """从案件列表查找案件"""
        result = False
        key_word = list()
        key_word.append(keyword)
        res = self.identify_api.list_criminal_case(key_word=key_word, remove_type=0)
        has_error = res.get('hasError')
        if has_error:
            result = False
        else:
            case_list = res.get('data').get('caseList')
            if case_list is None:
                result = False
            else:
                for case in case_list:
                    case_name = case.get('caseName')
                    if case_name == keyword:
                        result = True
                        break
                    else:
                        result = False
        return result

    def find_case_in_recycle_bin(self, keyword: str):
        """从案件回收站查找案件"""
        result = False
        key_word = list()
        key_word.append(keyword)
        res = self.identify_api.list_criminal_case(key_word=key_word, remove_type=10)
        has_error = res.get('hasError')
        if has_error:
            result = False
        else:
            case_list = res.get('data').get('caseList')
            if case_list is None:
                result = False
            else:
                for case in case_list:
                    case_name = case.get('caseName')
                    if case_name == keyword:
                        result = True
                        break
                    else:
                        result = False
        return result

    def remove_case(self, case_id: str):
        """从案件列表删除案件"""
        res = self.identify_api.remove_criminal_case(case_id, remove_type=10)
        return res

    def restore_case(self, case_id: str):
        """从案件回收站还原案件"""
        res = self.identify_api.remove_criminal_case(case_id, remove_type=0)
        return res

    def complete_remove_case(self, case_id: str):
        """从案件回收站彻底删除案件"""
        res = self.identify_api.remove_criminal_case(case_id, remove_type=20)
        return res

    def sync_my_case(self):
        """案件列表同步我的案件"""
        res = self.identify_api.list_criminal_case(remove_type=0, case_type=1)
        return res

    def sync_other_case(self):
        """案件列表同步他人案件"""
        res = self.identify_api.list_criminal_case(remove_type=0, case_type=2)
        return res

    def sync_all_case(self):
        """案件列表同步所有案件"""
        res = self.identify_api.list_criminal_case(remove_type=0, case_type=16)
        return res

    def add_folder(self, case_id: str, folder_name: str, folder_id: str = 'root'):
        """
        案件下新增文件夹
        :param case_id: 案件id
        :param folder_name: 文件夹名称
        :param folder_id: 父文件夹id，root指案件根目录
        :return: 新增文件夹的id
        """
        res = self.identify_api.new_criminal_case_folder(case_id, folder_name, folder_id)
        has_error = res.get('hasError')
        new_folder_id = None
        if has_error is False:
            new_folder_id = res.get('data').get('folderId')
        return new_folder_id

    def find_folder_by_id(self, case_id: str, target_folder_id: str):
        """
        通过文件夹id查找文件夹
        :param case_id:
        :param target_folder_id: 需要查找的文件夹id
        :return:
        """
        res = self.identify_api.list_all_criminal_case_folder(case_id)
        has_error = res.get('hasError')
        find_result = False
        if has_error is False:
            folder_list = res.get('data').get('folderList')
            for folder in folder_list:
                folder_id = folder.get('folderId')
                if folder_id == target_folder_id:
                    find_result = True
                    break
        return find_result

    def get_file_id(self, file_path: str, mime_type: str = 'audio/wav'):
        """
        上传文件获得file_id
        :param file_path: 音频文件路径
        :param mime_type:
        :return: file_id
        """
        res = self.identify_api.voice_file_upload(file_path, mime_type)
        file_id = None
        has_error = res.get('hasError')
        if has_error is False:
            file_id = res.get('data').get('fileList')[0].get('fileId')
        return file_id

    def upload_file_to_folder(self, case_id: str, file_path: str, mime_type: str = 'audio/wav',
                              folder_id: str = 'root'):
        """上传文件到指定文件夹"""
        file_id = self.get_file_id(file_path, mime_type)
        file_name = get_file_name(file_path)
        self.identify_api.add_voice(case_id, file_id, file_name, folder_id)
        return file_id

    def find_file_by_id(self, case_id, target_folder_id, target_file_id):
        """
        在指定文件夹下，根据文件id查找文件
        :param case_id:
        :param target_folder_id:
        :param target_file_id:
        :return:
        """
        find_result = False
        res = self.identify_api.list_all_criminal_case_folder(case_id)
        has_error = res.get('hasError')
        if has_error is False:
            folder_list = res.get('data').get('folderList')
            for folder in folder_list:
                parent_id = folder.get('parentId')
                file_id = folder.get('fileId')
                if parent_id == target_folder_id and file_id == target_file_id:
                    find_result = True
                    break
        return find_result

    def rename_file(self, file_id, new_name):
        """
        文件重命名
        :param file_id:
        :param new_name:
        :return:
        """
        res = self.identify_api.rename_voice(file_id, new_name)
        return res

    def find_file_by_name(self, case_id, target_folder_id, target_file_name):
        """
        在指定文件夹下，根据文件名查找文件
        :param case_id:
        :param target_folder_id:
        :param target_file_name:
        :return:
        """
        find_result = False
        res = self.identify_api.list_all_criminal_case_folder(case_id)
        has_error = res.get('hasError')
        if has_error is False:
            folder_list = res.get('data').get('folderList')
            for folder in folder_list:
                parent_id = folder.get('parentId')
                file_name = folder.get('name')
                if parent_id == target_folder_id and file_name == target_file_name:
                    find_result = True
                    break
        return find_result

    def remove_voice(self, file_id):
        """删除音频"""
        res = self.identify_api.remove_voice(file_id)
        return res

    def remove_attachment(self, file_id):
        """删除附件（非音频文件）"""
        res = self.identify_api.remove_attachment(file_id)
        return res

    def clear_case_list(self, start_name):
        """
        清空案件列表测试数据
        :param start_name:
        :return:
        """
        case_list_res = self.identify_api.list_criminal_case(case_type=1, remove_type=0)
        case_list = case_list_res.get('data').get('caseList')
        for case in case_list:
            if case.get('caseName').startswith(start_name):
                case_id = case.get('criminalCaseId')
                self.identify_api.remove_criminal_case(case_id, remove_type=10)

    def clear_recycle_bin(self, start_name):
        """
        清空回收站案件测试数据
        :param start_name:
        :return:
        """
        case_list_res = self.identify_api.list_criminal_case(case_type=1, remove_type=10)
        case_list = case_list_res.get('data').get('caseList')
        for case in case_list:
            if case.get('caseName').startswith(start_name):
                case_id = case.get('criminalCaseId')
                self.identify_api.remove_criminal_case(case_id, remove_type=20)

    def del_test_case(self):
        """
        因服务器等不可控原因，测试用例执行不下去的时候案件不会被成功删除，该方法在模块用例执行完后遍历案件列表，删除所有接口测试案件
        :return:
        """
        start_name = get_config('base_info', 'case_name_prefix')
        # 删除案件列表数据
        self.clear_case_list(start_name)
        # 删除案件回收站数据
        self.clear_recycle_bin(start_name)

    def get_auth_group_id_by_name(self, target_group_name: str):
        """
        根据权限组名称获取权限组id
        :param target_group_name:
        :return:
        """
        res = self.identify_api.get_auth_group_list()
        user_group_id = None
        has_error = res.get('hasError')
        if has_error is False:
            group_list = res.get('data').get('grouplist')
            for group in group_list:
                group_name = group.get('groupname')
                if group_name == target_group_name:
                    user_group_id = group.get('groupid')
                    break
        return user_group_id

    def get_user_id_by_name(self, group_id: str, target_username: str):
        """
        根据用户名获取用户id
        :param group_id: 用户组id
        :param target_username: 用户名
        :return: 用户id
        """
        user_id = None
        res = self.identify_api.get_auth_group_user_list(group_id)
        has_error = res.get('hasError')
        if has_error is False:
            user_list = res.get('data').get('userlist')
            for user in user_list:
                username = user.get('username')
                if username == target_username:
                    user_id = user.get('userid')
                    break
        return user_id

    def case_allocate(self, case_id: str, user_ids: list):
        """
        分发案件
        :param case_id:
        :param user_ids: 用户id列表
        :return:
        """
        res = self.identify_api.allot_case(case_id, user_ids)
        return res

    def add_tag(self, begin_time: int, end_time: int, case_id: str, tag_name: str, file_id: str, comment: str = '',
                color: str = "#D37F00", phoneme_id: str = ''):
        """添加标记"""
        res = self.identify_api.add_voice_tag(begin_time, end_time, comment, case_id, file_id, tag_name,
                                              phoneme_id, color)
        tag_id = None
        has_error = res.get('hasError')
        if has_error is False:
            tag_id = res.get('data').get('voiceTagId')
        return tag_id

    def find_tag_by_id(self, case_id: str, file_id: str, target_tag_id, limit: int = 1000, offset: int = 0):
        """通过id查找标记"""
        res = self.identify_api.list_voice_tag(case_id, file_id, limit, offset)
        find_result = find_object_from_list(res, 'voiceTagList', target_tag_id, 'voiceTagId')
        return find_result

    def get_tag_info(self, case_id: str, file_id: str, target_tag_id, limit: int = 1000, offset: int = 0):
        """获取标记信息"""
        res = self.identify_api.list_voice_tag(case_id, file_id, limit, offset)
        tag_info = dict()
        has_error = res.get('hasError')
        if has_error is False:
            tag_list = res.get('data').get('voiceTagList')
            if tag_list:
                for tag_info in tag_list:
                    tag_id = tag_info.get('voiceTagId')
                    if tag_id == target_tag_id:
                        return tag_info
        return tag_info

    def update_tag(self, begin_time: int, end_time: int, tag_id: str, tag_name: str, comment: str):
        """更新标记"""
        res = self.identify_api.update_voice_tag(begin_time, end_time, comment, tag_id, tag_name)
        return res

    def remove_tag(self, tag_ids: list, optional: int = 1):
        """删除标记"""
        res = self.identify_api.remove_voice_batch_tag(tag_ids, optional)
        return res

    def find_tag_in_recycle_by_id(self, case_id: str, tag_id: str):
        """根据标记id在回收站查找标记"""
        res = self.identify_api.recycle_list_tag(case_id)
        find_result = find_object_from_list(res, 'tags', tag_id, 'tagId')
        return find_result

    def recover_tag(self, tag_ids):
        """还原标记"""
        res = self.identify_api.recover_voice_tags(tag_ids)
        return res

    def add_hearing_analysis(self, material_file_id: str, sample_file_id: str, case_id: str,
                             recode_state: bool = True,
                             pitch_level_score: int = 0, pitch_level_comment: str = "0",
                             pitch_variation_range_score: int = 1, pitch_variation_range_comment: str = "1",
                             pitch_model_score: int = 2, pitch_model_comment: str = "2",
                             throat_allover_score: int = 3, throat_allover_comment: str = "3",
                             throat_bubble_score: int = 4, throat_bubble_comment: str = "4",
                             throat_other_score: int = 5, throat_other_comment: str = "5",
                             tone_intensity_score: int = 6, tone_intensity_comment: str = "6",
                             dialect_area_score: int = 7, dialect_area_comment: str = "7",
                             dialect_foreign_language_score: int = 8, dialect_foreign_language_comment: str = "8",
                             dialect_idiom_score: int = 9, dialect_idiom_comment: str = "9",
                             tuning_vowel_score: int = 10, tuning_vowel_comment: str = "10",
                             tuning_consonant_score: int = 9, tuning_consonant_comment: str = "11",
                             tuning_mispronunciation_score: int = 8, tuning_mispronunciation_comment: str = "12",
                             tuning_nasal_score: int = 7, tuning_nasal_comment: str = "13",
                             rhythm_speaking_rate_score: int = 6, rhythm_speaking_rate_comment: str = "14",
                             rhythm_speech_burst_score: int = 5, rhythm_speech_burst_comment: str = "15",
                             rhythm_other_score: int = 4, rhythm_other_comment: str = "16",
                             other_incoherence_score: int = 3, other_incoherence_comment: str = "17",
                             other_language_barrier_score: int = 2, other_language_barrier_comment: str = "18",
                             other_feature_score: int = 1, other_feature_comment: str = "19"):
        res = self.identify_api.add_hearing_analysis(material_file_id, sample_file_id, case_id,
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
        has_error = res.get('hasError')
        hearing_id = None
        if has_error is False:
            hearing_id = res.get('data').get('hearingId')
        return hearing_id

    def find_hearing_analysis_by_id(self, case_id, target_hearing_id):
        """根据id查找听觉量化分析记录"""
        res = self.identify_api.list_hearing_analysis(case_id)
        find_result = find_object_from_list(res, 'listHearingAnalysis', target_hearing_id, 'hearingId')
        return find_result

    def del_hearing_analysis(self, case_id: str, material_file_id: str, sample_file_id: str):
        """删除听觉量化分析记录"""
        res = self.identify_api.del_hearing_analysis(case_id, material_file_id, sample_file_id)
        return res

    def change_password(self, user_id, old_password, new_password):
        """修改当前登录用户密码"""
        res = self.identify_api.change_password(user_id, old_password, new_password)
        return res

    def reset_password(self, user_id):
        """重置用户密码为123456"""
        res = self.identify_api.reset_key(user_id)
        return res

    def add_auth_group(self, group_name):
        """添加用户组"""
        res = self.identify_api.add_auth_group(group_name)
        return res

    def find_auth_group_by_name(self, group_name):
        """根据权限分组名称查找权限分组"""
        res = self.identify_api.get_auth_group_list()
        find_result = find_object_from_list(res, 'grouplist', group_name, 'groupname')
        return find_result

    def update_name_auth_group(self, group_id, new_group_name):
        """更改权限组名称"""
        res = self.identify_api.update_name_auth_group(new_group_name, group_id)
        return res

    def del_auth_group(self, group_id):
        """删除用户权限分组"""
        res = self.identify_api.del_auth_group(group_id)
        return res

    def update_auth_group(self, group_id, allocate_case_auth: bool = True, create_case_auth: bool = True,
                          delete_case_auth: bool = True, edit_case_auth: bool = True, give_case_auth: bool = True,
                          manage_user_auth: bool = True, over_case_auth: bool = True, rename_case_auth: bool = True,
                          share_case_auth: bool = True):
        """修改权限组权限"""
        res = self.identify_api.update_auth_group(group_id, allocate_case_auth, create_case_auth, delete_case_auth,
                                                  edit_case_auth, give_case_auth, manage_user_auth, over_case_auth,
                                                  rename_case_auth, share_case_auth)
        return res

    def get_group_auth(self, group_id):
        """获取权限组权限"""
        res = self.identify_api.get_auth_group_user_list(group_id)
        has_error = res.get('hasError')
        if has_error is False:
            auth_list = res.get('data').get('authlist')
            return auth_list

    def add_user(self, group_id, username):
        """添加用户"""
        res = self.identify_api.add_user_auth_group(group_id, username)
        return res

    def find_user_by_name(self, group_id, target_username):
        """根据用户名查找用户"""
        res = self.identify_api.get_auth_group_user_list(group_id)
        find_result = find_object_from_list(res, 'userlist', target_username, 'username')
        return find_result

    def del_user(self, group_id, user_id):
        """删除用户"""
        res = self.identify_api.del_user_auth_group(group_id, user_id)
        return res

    def update_user(self, to_group_id, user_id, user_name):
        """编辑用户"""
        res = self.identify_api.update_user_auth_group(to_group_id, user_id, user_name)
        return res


if __name__ == '__main__':
    # from api.other import create_case_name, create_random_str
    operate_api = OperateApi()
    a = operate_api.get_auth_group_id_by_name('都君')
    print(a)
