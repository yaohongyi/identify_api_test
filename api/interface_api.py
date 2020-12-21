#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import requests
import logging
import json
from api.other import get_config, get_response, get_file_name

server_address = get_config('base_info', 'server_address')


# 用户登录拿到sessionId
def login(nickname: str, password: str):
    url = f"{server_address}/call?id=experts.login&v="
    data = {
        "nickname": nickname,
        "passwd": password
    }
    res = get_response(url, data)
    return res


class IdentifyApi:
    def __init__(self, session_id):
        self.session_id = session_id

    def add_auth_group(self, group_name):
        """
        添加用户组
        :param group_name:
        :return:
        """
        url = f"{server_address}/call?id=experts.AddAuthGroup&v="
        data = {
            "sessionid": self.session_id,
            "groupname": group_name
        }
        res = get_response(url, data)
        return res

    def get_auth_group_list(self):
        """
        获取权限分组列表
        :return:
        """
        url = f"{server_address}/call?id=experts.GetAuthGroupList&v="
        data = {
            "sessionid": self.session_id
        }
        res = get_response(url, data)
        return res

    def update_auth_group(self, group_id, allocate_case_auth: bool = True, create_case_auth: bool = True,
                          delete_case_auth: bool = True, edit_case_auth: bool = True, give_case_auth: bool = True,
                          manage_user_auth: bool = True, over_case_auth: bool = True, rename_case_auth: bool = True,
                          share_case_auth: bool = True):
        """
        修改权限分组的权限
        :param group_id:
        :param allocate_case_auth: 分发案件权限
        :param create_case_auth: 创建案件权限
        :param delete_case_auth: 删除案件权限
        :param edit_case_auth: 修改案件权限
        :param give_case_auth:
        :param manage_user_auth: 用户管理权限
        :param over_case_auth:
        :param rename_case_auth: 修改案件权限
        :param share_case_auth: 修改案件权限
        :return:
        """
        url = f"{server_address}/call?id=experts.UpdateAuthGroup&v="
        data = {
            "sessionid": self.session_id,
            "groupid": group_id,
            "authlist": {
                'AuthAllocateCase': allocate_case_auth,
                'AuthCreateCase': create_case_auth,
                'AuthDeleteCase': delete_case_auth,
                'AuthEditCase': edit_case_auth,
                'AuthGiveCase': give_case_auth,
                'AuthManageUser': manage_user_auth,
                'AuthOverCase': over_case_auth,
                'AuthRenameCase': rename_case_auth,
                'AuthShareCase': share_case_auth
            }
        }
        res = get_response(url, data)
        return res

    def add_user_auth_group(self, group_id, username):
        """
        添加权限分组用户
        :param group_id:
        :param username:
        :return:
        """
        url = f"{server_address}/call?id=experts.AddUserAuthGroup&v="
        data = {
            "sessionid": self.session_id,
            "groupid": group_id,
            "username": username
        }
        res = get_response(url, data)
        return res

    def new_criminal_case(self, case_name: str, private_case: bool = False, share_case: bool = False,
                          case_classify_id: str = "", share_user_list: list = None):
        """
        新建案件
        :param case_name: 案件名
        :param private_case: 案件属性
        :param share_case: 是否为共享案件
        :param case_classify_id: 所属案件分类（二级分类id）
        :param share_user_list: 分享用户id列表
        :return: res
        """
        url = f"{server_address}/call?id=experts.newCriminalCase&v="
        if share_user_list is None:
            share_user_list = []
        data = {
            "sessionId": self.session_id,
            "caseName": case_name,
            "shareUserList": share_user_list,
            "privateCase": private_case,
            "ShareCase": share_case,
            "typeId": case_classify_id
        }
        res = get_response(url, data)
        return res

    def list_criminal_case(self, offset=0, limit=99999, key_word: list = None, remove_type: int = 0, case_type=1,
                           first_case_classify_id: str = "", second_case_classify_id: str = ""):
        """
        获取案件列表
        :param offset: 偏移
        :param limit: 数量
        :param key_word: 关键字
        :param remove_type: 0-案件列表，10-案件回收站
        :param case_type: 1-我的案件，2-分发案件，16-所有案件，128-共享案件
        :param first_case_classify_id: 一级案件分类id
        :param second_case_classify_id: 二级案件分类id
        :return:
        """
        url = f"{server_address}/call?id=experts.listCriminalCase&v="
        data = {
            "sessionid": self.session_id,
            "offset": offset,
            "limit": limit,
            "removeType": remove_type,
            "key_word": key_word,
            "type": case_type,
            "firstLevel": first_case_classify_id,
            "secondLevel": second_case_classify_id
        }
        res = get_response(url, data)
        return res

    # 打开案件
    def open_criminal_case(self, case_id):
        url = f"{server_address}/call?id=experts.openCriminalCase&v="
        data = {
            "sessionId": self.session_id,
            "criminalCaseId": case_id
        }
        res = get_response(url, data)
        return res

    def rename_criminal_case(self, new_case_name, case_id):
        """
        案件重命名
        :param new_case_name:
        :param case_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.renameCriminalCase&v="
        data = {
            "sessionId": self.session_id,
            "criminalCaseName": new_case_name,
            "criminalCaseId": case_id
        }
        res = get_response(url, data)
        return res

    # 导出案件
    def export_case(self, case_id):
        url = f"{server_address}/call?id=experts.exportArchive&v=&sessionId={self.session_id}&fileId={case_id}"
        res = requests.get(url).content
        return res

    def bind_source_case(self, identify_case_id, source_id, source_info):
        url = f"{server_address}/call?id=experts.bindSourceCriminalCase&v="
        data = {
            'criminalCaseId': identify_case_id,
            'sessionId': self.session_id,
            'sourceId': source_id,
            'sourceInfo': source_info
        }
        res = get_response(url, data)
        return res

    def voice_file_upload(self, file_path, mime_type: str = 'audio/wav'):
        """
        上传文件（包括但不限于音频文件）
        :param file_path:
        :param mime_type: 文件mime类型。参考https://www.w3school.com.cn/media/media_mimeref.asp
        :return:
        """
        url = f"{server_address}/file?id=experts.voiceFileUpload&v=&sessionId={self.session_id}"
        with open(file_path, "rb") as f:
            file_content = f.read()
        file_name = get_file_name(file_path)
        multiple_files = [(file_name, (file_name, file_content, mime_type))]
        res = json.loads(requests.post(url, files=multiple_files).content)
        res_json = json.dumps(res, indent=4, ensure_ascii=False, separators=(',', ':'))
        logging.info(f'Interface voice_file_upload response data:\n {res_json}')
        return res

    # 列出语音
    def list_voice(self, cate_gory='MATERIAL', **kwargs):
        url = f"{server_address}/call?id=experts.listVoice&v="
        data = {
            "sessionId": self.session_id,
            "cateGory": cate_gory,
            "criminalCaseId": kwargs["criminalCaseId"],
            "offset": 0,
            "limit": 99
        }
        res = get_response(url, data)
        for k in kwargs.keys():
            if k == 'verifyFile':
                uploaded_voice_list = []
                voice_list = res.get('data').get('voiceList')
                for file in voice_list:
                    for i in range(len(kwargs['verifyFile'])):
                        if file['voiceFileName'] == kwargs['verifyFile'][i]:
                            uploaded_voice_list.append(file)
                logging.info('uploaded_voiceList %s' % uploaded_voice_list)
                return uploaded_voice_list
            elif k == 'compareFile':
                if not len(kwargs['compareFile']) == 2:
                    logging.error('Error： compareFile can only contain 2 files ...')
                    raise ValueError('Error： compareFile can only contain 2 files ...')
                compare_voice_list = []
                voice_list = res.get('data').get('voiceList')
                for file in voice_list:
                    for i in range(len(kwargs['compareFile'])):
                        if file['voiceFileName'] == kwargs['compareFile'][i]:
                            compare_voice_list.append(file)
                logging.info('compare_voiceList %s' % compare_voice_list)
                return compare_voice_list
        return res

    def add_voice(self, case_id, voice_file_id, voice_file_name, folder_id: str = 'root', category='MATERIAL'):
        """
        新增音频
        :param case_id:
        :param voice_file_id:
        :param voice_file_name:
        :param folder_id:
        :param category:
        :return:
        """
        url = f'{server_address}/call?id=experts.addVoice&v='
        data = {
            'sessionId': self.session_id,
            'criminalCaseId': case_id,
            'voiceFileId': voice_file_id,
            'voiceFileName': voice_file_name,
            'cateGory': category,
            'folderId': folder_id
        }
        res = get_response(url, data)
        return res

    def rename_voice(self, voice_file_id, voice_name):
        """"""
        url = f"{server_address}/call?id=experts.renameVoice&v="
        data = {
            'sessionId': self.session_id,
            'voiceFileId': voice_file_id,
            'voiceName': voice_name
        }
        res = get_response(url, data)
        return res

    def add_images(self, case_id, image_file_id, image_file_name, folder_id: str):
        """"""
        url = f"{server_address}/call?id=experts.AddImages&v="
        data = {
            'sessionId': self.session_id,
            'images': [{
                'criminalCaseId': case_id,
                'imageFileId': image_file_id,
                'imageFileName': image_file_name,
                'folderId': folder_id
            }]
        }
        res = get_response(url, data)
        return res

    def save_image_windows(self, image_data: str, image_id: str):
        """"""
        url = f"{server_address}/call?id=experts.saveImageWindows&v="
        data = {
            'payload': [{
                'data': image_data,
                'imageId': image_id
            }],
            'sessionId': self.session_id
        }
        res = get_response(url, data)
        return res

    def list_image(self, case_id, offset=0, limit=99):
        """"""
        url = f"{server_address}/call?id=experts.listImage&v="
        data = {
            'sessionId': self.session_id,
            'criminalCaseId': case_id,
            'limit': limit,
            'offset': offset
        }
        res = get_response(url, data)
        return res

    def remove_image(self, image_id):
        """"""
        url = f"{server_address}/call?id=experts.removeImage&v="
        data = {
            'sessionId': self.session_id,
            'imageId': image_id
        }
        res = get_response(url, data)
        return res

    def remove_image_batch(self, image_id: list, status: int = 1):
        """
        删除图片
        :param image_id:
        :param status: 1-删除（到回收站），2-彻底删除
        :return:
        """
        url = f"{server_address}/call?id=experts.removeImageBatch&v="
        data = {
            'imageId': image_id,
            'sessionId': self.session_id,
            'status': status
        }
        res = get_response(url, data)
        return res

    def get_mos_snr(self, voice_id):
        """获取文件mos和snr"""
        url = f"{server_address}/call?id=experts.getmossnr&v="
        data = {
            "sessionId": self.session_id,
            "voiceid": voice_id
        }
        logging.info('get_mos_snr %s ' % data)
        res = get_response(url, data)
        return res

    # 列出音素
    def list_phoneme(self, voice_file_id, list_type='UNFILTERED', limit=100000, offset=0, re_gen_phoneme=False):
        url = f"{server_address}/call?id=experts.listPhoneme&v="
        data = {
            'sessionId': self.session_id,
            'voiceFileId': voice_file_id,
            'listType': list_type,
            'limit': limit,
            'offset': offset,
            'reGenPhoneme': re_gen_phoneme
        }
        res = get_response(url, data)
        return res

    def add_voice_tag(self, begin_time, end_time, comment, case_id, voice_file_id, voice_tag_name,
                      phoneme_id='', color='#D37F00'):
        """
        增加标记
        :param begin_time: 开始时间
        :param end_time: 结束时间
        :param comment: 标记备注
        :param case_id: 案件id
        :param voice_file_id: 音频文件id
        :param voice_tag_name: 标记名称
        :param phoneme_id:
        :param color:
        :return:
        """
        url = f"{server_address}/call?id=experts.addVoiceTag&v="
        data = {
            'sessionId': self.session_id,
            'beginTime': begin_time,
            'endTime': end_time,
            'color': color,
            'comment': comment,
            'criminalCaseId': case_id,
            'phonemeId': phoneme_id,
            'voiceFileId': voice_file_id,
            'voiceTagName': voice_tag_name
        }
        res = get_response(url, data)
        return res

    def list_voice_tag(self, case_id: str, voice_file_id: str, limit: int = 1000, offset: int = 0):
        """
        列出标记
        :param case_id:
        :param voice_file_id:
        :param limit:
        :param offset:
        :return:
        """
        url = f"{server_address}/call?id=experts.listVoiceTag&v="
        data = {
            'sessionId': self.session_id,
            'criminalCaseId': case_id,
            'voiceFileId': voice_file_id,
            'limit': limit,
            'offset': offset
        }
        res = get_response(url, data)
        return res

    def remove_voice_tag(self, voice_tag_id):
        """
        删除标记
        :param voice_tag_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.removeVoiceTag&v="
        data = {
            'sessionId': self.session_id,
            'voiceTagId': voice_tag_id
        }
        res = get_response(url, data)
        return res

    def remove_voice_batch_tag(self, voice_tag_ids, optional: int = 1):
        """
        批量删除标记
        :param voice_tag_ids:
        :param optional: 1-从标记列表删除，2-从回收站彻底删除
        :return:
        """
        url = f"{server_address}/call?id=experts.removeVoiceBatchTag&v="
        data = {
            'optional': optional,
            'sessionId': self.session_id,
            'voiceTagIds': voice_tag_ids
        }
        res = get_response(url, data)
        return res

    def remove_voice(self, file_id):
        """
        删除语音
        :param file_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.removeVoice&v="
        data = {
            "sessionId": self.session_id,
            "voiceFileId": file_id
        }
        res = get_response(url, data)
        return res

    def remove_attachment(self, file_id):
        """"""
        url = f"{server_address}/call?id=experts.removeAttachment&v="
        data = {
            "attachmentFileId": file_id,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def remove_criminal_case(self, case_id, remove_type=10):
        """
        删除&还原案件
        :param case_id:
        :param remove_type: 0-从案件回收站还原案件，10-放到案件回收站，20-案件回收站彻底删除
        :return:
        """
        url = f"{server_address}/call?id=experts.removeCriminalCase&v="
        data = {
            "sessionId": self.session_id,
            "criminalCaseId": case_id,
            "removeType": remove_type
        }
        res = get_response(url, data)
        return res

    def allot_case(self, case_id, user_id_list, owner_id: str = ''):
        """分发案件"""
        url = f"{server_address}/call?id=experts.criminalCaseAllocate&v="
        data = {
            "criminalCaseId": case_id,
            "ownerId": owner_id,
            "sessionId": self.session_id,
            "userIdList": user_id_list
        }
        res = get_response(url, data)
        return res

    def get_allot_progress(self, task_id):
        """获取分发案件进度"""
        url = f"{server_address}/call?id=experts.criminalcaseAllocateProgress&v="
        data = {
            "session_id": self.session_id,
            "task_id": task_id
        }
        logging.debug(f"Begin get allot case task '{task_id}' progress!")
        res = get_response(url, data)
        logging.info(f"The get_allot_case_progress interface res is:\n{res}")
        return res

    def get_auth_group_user_list(self, group_id):
        """
        获取权限分组用户列表
        :param group_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.GetAuthGroupUserList&v="
        data = {
            "sessionId": self.session_id,
            "groupid": group_id
        }
        res = get_response(url, data)
        return res

    def del_user_auth_group(self, group_id, user_id):
        """
        删除用户
        :param group_id:
        :param user_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.DelUserAuthGroup&v="
        data = {
            "sessionId": self.session_id,
            "groupid": group_id,
            "userid": user_id
        }
        res = get_response(url, data)
        return res

    def del_auth_group(self, group_id):
        """
        删除权限分组
        :param group_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.DelAuthGroup&v="
        data = {
            "sessionId": self.session_id,
            "groupid": group_id
        }
        res = get_response(url, data)
        return res

    def update_user_auth_group(self, to_group_id, user_id, username):
        """
        修改用户信息
        :param to_group_id:
        :param user_id:
        :param username:
        :return:
        """
        url = f"{server_address}/call?id=experts.UpdateUserAuthGroup&v="
        data = {
            "sessionId": self.session_id,
            "togroupid": to_group_id,
            "userid": user_id,
            "username": username
        }
        res = get_response(url, data)
        return res

    def update_name_auth_group(self, group_name, group_id):
        """
        修改权限分组名称
        :param group_name:
        :param group_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.UpdateNameAuthGroup&v="
        data = {
            "sessionId": self.session_id,
            "groupname": group_name,
            "groupid": group_id
        }
        res = get_response(url, data)
        logging.info("UpdateNameAuthGroup：AuthGroup update name to '{}'".format(group_name))
        return res

    # 鉴定报告保存
    @staticmethod
    def save_identify_report(**kwargs):
        url = f"{server_address}/call?id=experts.saveidentifyreport&v="
        data = {
            "analysiscontext": kwargs["analysiscontext"],  # 分析内容
            "analysistitle": kwargs["analysistitle"],  # 分析标题
            "casecontext": kwargs["casecontext"],  # 案件内容
            "casedesc": kwargs["casedesc"],  # 案件简介
            "caseid": kwargs["caseid"],  # 案件id
            "identifier": kwargs["identifier"],  # 鉴定
            "identifycontext": kwargs["identifycontext"],  # 鉴定内容
            "identifytime": kwargs["identifytime"],  # 鉴定时间
            "identifytitle": kwargs["identifytitle"],  # 鉴定标题
            "sessionId": kwargs["sessionId"],
            "title": kwargs["title"]
        }
        res = get_response(url, data)
        return res

    # 鉴定报告获取
    def get_identify_report(self, case_id):
        url = f"{server_address}/call?id=experts.getidentifyreport&v="
        data = {
            "caseid": case_id,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    # 获取存档
    def get_criminal_case_save(self, criminal_case_save_id):
        url = f"{server_address}/call?id=experts.getCriminalCaseSave&v="
        data = {
            "sessionId": self.session_id,
            "criminalCaseSaveId": criminal_case_save_id
        }
        res = get_response(url, data)
        return res

    # 列出存档
    def list_criminal_case_save(self, criminal_case_id, limit=100, offset=0):
        url = f"{server_address}/call?id=experts.listCriminalCaseSave&v="
        data = {
            "sessionId": self.session_id,
            "criminalCaseId": criminal_case_id,
            "limit": limit,
            "offset": offset
        }
        res = get_response(url, data)
        return res

    # 重命名存档
    def rename_criminal_case_save(self, case_save_id, criminal_case_save_name):
        url = f"{server_address}/call?id=experts.renameCriminalCaseSave&v="
        data = {
            "sessionId": self.session_id,
            "caseSaveId": case_save_id,
            "criminalCaseSaveName": criminal_case_save_name
        }
        res = get_response(url, data)
        return res

    # 设置存档
    def set_criminal_case_save(self, case_save_id, criminal_case_id, criminal_case_save_name, new_case_save,
                               sonogram_setting_list):
        url = f"{server_address}/call?id=experts.setCriminalCaseSave&v="
        data = {
            "sessionId": self.session_id,
            "caseSaveId": case_save_id,
            "criminalCaseId": criminal_case_id,
            "criminalCaseSaveName": criminal_case_save_name,
            "newCaseSave": new_case_save,
            "sonogramSettingList": sonogram_setting_list
        }
        res = get_response(url, data)
        return res

    # 移除存档
    def remove_criminal_case_save(self, case_save_id):
        url = f"{server_address}/call?id=experts.removeCriminalCaseSave&v="
        data = {
            "sessionId": self.session_id,
            "caseSaveId": case_save_id
        }
        res = get_response(url, data)
        return res

    # 上传日志
    @staticmethod
    def upload_log(ip, desc, version):
        url = f"{server_address}/call?id=experts.uploadlog&v="
        data = {
            "ip": ip,
            "desc": desc,
            "version": version
        }
        res = get_response(url, data)
        return res

    # 列出过滤的音素
    def add_phoneme_filter(self, phoneme_id):
        url = f"{server_address}/call?id=experts.addPhonemeFilter&v="
        data = {
            "sessionId": self.session_id,
            "phonemeId": phoneme_id
        }
        res = get_response(url, data)
        return res

    # 标记音素
    def mark_phoneme(self, phoneme_id, marked=True):
        url = f"{server_address}/call?id=experts.markPhoneme&v="
        data = {
            "sessionId": self.session_id,
            "phonemeId": phoneme_id,
            "marked": marked
        }
        res = get_response(url, data)
        return res

    # 撤销音素移除
    def remove_phoneme_filter(self, voice_file_id):
        url = f"{server_address}/call?id=experts.removePhonemeFilter&v="
        data = {
            "sessionId": self.session_id,
            "voiceFileId": voice_file_id
        }
        res = get_response(url, data)
        return res

    # 修改音素名
    def update_phoneme_name(self, phoneme_id, phoneme_name):
        url = f"{server_address}/call?id=experts.UpdatePhonemeName&v="
        data = {
            "sessionId": self.session_id,
            "phonemeId": phoneme_id,
            "phonemeName": phoneme_name
        }
        res = get_response(url, data)
        return res

    # upload上传操作日志
    def upload_operation_log(self, case_id, log):
        url = f"{server_address}/call?id=experts.UploadOprationLog&v="
        data = {
            "sessionId": self.session_id,
            "caseid": case_id,
            "log": log
        }
        res = get_response(url, data)
        return res

    # 列出操作日志
    def list_operation_log(self, case_id):
        url = f"{server_address}/call?id=experts.ListOprationLog&v="
        data = {
            "sessionId": self.session_id,
            "caseid": case_id
        }
        res = get_response(url, data)
        return res

    # 增加lpc标记
    def add_lpc_tag(self, remark, case_id, change_value, img_data, lpc_list):
        url = f"{server_address}/call?id=experts.addlpctag&v="
        data = {
            "sessionId": self.session_id,
            "remark": remark,
            "caseId": case_id,
            "changevalue": change_value,
            "imgdata": img_data,
            "list": lpc_list,
        }
        res = get_response(url, data)
        return res

    # 获取lpc标记
    def get_lpc_tag(self, lpc_id):
        url = f"{server_address}/call?id=experts.getlpctag&v="
        data = {
            "sessionId": self.session_id,
            "id": lpc_id
        }
        res = get_response(url, data)
        return res

    # 列出lpc标记
    def list_lpc_tag(self, case_id):
        url = f"{server_address}/call?id=experts.listlpctag&v="
        data = {
            "sessionId": self.session_id,
            "caseId": case_id
        }
        res = get_response(url, data)
        return res

    # 修改lpc标记
    def update_lpc_tag(self, lpc_id, remark, change_value, img_data, lpc_list):
        url = f"{server_address}/call?id=experts.updatelpctag&v="
        data = {
            "sessionId": self.session_id,
            "id": lpc_id,
            "remark": remark,
            "changevalue": change_value,
            "imgdata": img_data,
            "list": lpc_list
        }
        res = get_response(url, data)
        return res

    # 删除lpc标记
    def del_lpc_tag(self, lpc_id):
        url = f"{server_address}/call?id=experts.dellpctag&v="
        data = {
            "sessionId": self.session_id,
            "id": lpc_id
        }
        res = get_response(url, data)
        return res

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        修改密码
        :param user_id:
        :param old_password:
        :param new_password:
        :return:
        """
        url = f"{server_address}/call?id=experts.changePasswd&v="
        data = {
            "userId": user_id,
            "oldPasswd": old_password,
            "newPasswd": new_password
        }
        res = get_response(url, data)
        return res

    # 列出用户
    def list_user(self, offset, limit):
        url = f"{server_address}/call?id=experts.listUser&v="
        data = {
            "sessionId": self.session_id,
            "offset": offset,
            "Limit": limit
        }
        res = get_response(url, data)
        return res

    def reset_key(self, user_id):
        """重置用户密码为123456"""
        url = f"{server_address}/call?id=experts.resetKey&v="
        data = {
            "sessionId": self.session_id,
            "userId": user_id
        }
        res = get_response(url, data)
        return res

    # 注销（退出登录）
    def logout(self):
        url = f"{server_address}/call?id=experts.logout&v="
        data = {
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    # 批量增加标记
    def add_voice_tag_batch(self, tag_list):
        url = f"{server_address}/call?id=experts.addVoiceTagbatch&v="
        data = {
            "sessionId": self.session_id,
            "taglist": tag_list
        }
        res = get_response(url, data)
        return res

    # 更新标记
    def update_voice_tag(self, begin_time, end_time, comment, voice_tag_id, voice_tag_name):
        url = f"{server_address}/call?id=experts.updateVoiceTag&v="
        data = {
            'beginTime': begin_time,
            'comment': comment,
            'endTime': end_time,
            'sessionId': self.session_id,
            'voiceTagId': voice_tag_id,
            'voiceTagName': voice_tag_name
        }
        res = get_response(url, data)
        return res

    # 储存标记
    def save_voice_tag(self, case_id, voice_tag_list):
        url = f"{server_address}/call?id=experts.saveVoiceTag&v="
        data = {
            "sessionId": self.session_id,
            "criminalCaseId": case_id,
            "voiceTagList": voice_tag_list
        }
        res = get_response(url, data)
        return res

    # 获取文件信息
    def get_file_info(self, voice_id):
        url = f"{server_address}/call?id=experts.GetFileInfo&v="
        data = {
            "sessionId": self.session_id,
            "voiceid": voice_id
        }
        res = get_response(url, data)
        return res

    # 文件下载
    def voice_file_download(self, file_id):
        url = f"{server_address}/file?id=experts.voiceFileDownload&v=&sessionId={self.session_id}&fileId={file_id}"
        res = requests.get(url)
        return res

    # 语种识别
    def language_recognition(self, file_id, start_time=0, end_time=6000):
        url = f"{server_address}/call?id=experts.Language&v="
        data = {
            "sessionId": self.session_id,
            "fileId": file_id,
            "startTime": start_time,
            "endTime": end_time
        }
        res = get_response(url, data)
        return res

    # 身高&性别识别
    def gender_height(self, file_id, start_time=0, end_time=6000):
        url = f"{server_address}/call?id=experts.GenderHeight&v="
        data = {
            "sessionId": self.session_id,
            "fileId": file_id,
            "startTime": start_time,
            "endTime": end_time
        }
        res = get_response(url, data)
        return res

    # 混响&有效时长
    def reverberation(self, file_id, start_time=0, end_time=6000, full_text=True):
        url = f"{server_address}/call?id=experts.Reverberation&v="
        data = {
            "sessionId": self.session_id,
            "fileId": file_id,
            "startTime": start_time,
            "endTime": end_time,
            "fullText": full_text
        }
        res = get_response(url, data)
        return res

    # 拨号音识别
    def phone_number(self, file_id, start_time=0, end_time=6000):
        url = f"{server_address}/call?id=experts.PhoneNumber&v="
        data = {
            "sessionId": self.session_id,
            "fileId": file_id,
            "startTime": start_time,
            "endTime": end_time
        }
        res = get_response(url, data)
        return res

    # 人声分离
    def speech_diarization(self, file_id, start_time=0, end_time=6000, speaker_num=2):
        url = f"{server_address}/call?id=experts.Diarization&v="
        data = {
            "sessionId": self.session_id,
            "fileId": file_id,
            "startTime": start_time,
            "endTime": end_time,
            "speakerNum": speaker_num
        }
        res = get_response(url, data)
        return res

    # 去除无效片段
    def invalid_part(self, file_id, start_time=0, end_time=6000, full_text=True):
        url = f"{server_address}/call?id=experts.InvalidPart&v="
        data = {
            "sessionId": self.session_id,
            "fileId": file_id,
            "startTime": start_time,
            "endTime": end_time,
            "fullText": full_text
        }
        res = get_response(url, data)
        return res

    def new_criminal_case_folder(self, case_id: str, folder_name: str, folder_id: str = 'root'):
        """
        新建文件夹
        :param case_id:
        :param folder_id: 父文件夹id
        :param folder_name:
        :return:
        """
        url = f"{server_address}/call?id=experts.newCriminalCaseFolder&v="
        data = {
            "criminalCaseId": case_id,
            "folderId": folder_id,
            "folderName": folder_name,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def list_all_criminal_case_folder(self, case_id: str, folder_id: str = ""):
        """
        获取案件下的文件夹列表
        :param case_id:
        :param folder_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.listAllCriminalCaseFolder&v="
        data = {
            "criminalCaseId": case_id,
            "folderId": folder_id,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def filter_asr_region(self, file_id: str, end_time: int, start_time: int = 0):
        """"""
        url = f"{server_address}/call?id=experts.FilterAsrRegion&v="
        data = {
            "fileId": file_id,
            "sessionId": self.session_id,
            "startTime": start_time,
            "endTime": end_time
        }
        res = get_response(url, data)
        return res

    def recycle_list_tag(self, case_id):
        """
        回收站获取标记列表
        :param case_id: 案件id
        :return:
        """
        url = f"{server_address}/call?id=experts.recycleListTag&v="
        data = {
            "criminalCaseId": case_id,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def recover_voice_tags(self, tag_ids: list):
        """
        从回收站还原标记
        :param tag_ids: 标记id列表
        :return:
        """
        url = f"{server_address}/call?id=experts.recoverVoiceTags&v="
        data = {
            "sessionId": self.session_id,
            "voiceTagIds": tag_ids
        }
        res = get_response(url, data)
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
        """
        新增听觉量化分析记录
        :param material_file_id: 检材文件id
        :param sample_file_id: 样本文件id
        :param case_id: 案件id
        :param recode_state: 编码状态
        :param pitch_level_score: 音高水平得分
        :param pitch_level_comment:
        :param pitch_variation_range_score: 音高变异范围得分
        :param pitch_variation_range_comment:
        :param pitch_model_score: 音高模式得分
        :param pitch_model_comment:
        :param throat_allover_score: 嗓音特质总体得分
        :param throat_allover_comment:
        :param throat_bubble_score: 嗓音特质气泡音得分
        :param throat_bubble_comment:
        :param throat_other_score: 嗓音特质其他得分
        :param throat_other_comment:
        :param tone_intensity_score: 音强变异范围得分
        :param tone_intensity_comment:
        :param dialect_area_score: 方言地区得分
        :param dialect_area_comment:
        :param dialect_foreign_language_score: 方言外语得分
        :param dialect_foreign_language_comment:
        :param dialect_idiom_score: 方言个人习语得分
        :param dialect_idiom_comment:
        :param tuning_vowel_score: 调音方式元音得分
        :param tuning_vowel_comment:
        :param tuning_consonant_score: 调音方式辅音得分
        :param tuning_consonant_comment:
        :param tuning_mispronunciation_score: 调音方式错误发音得分
        :param tuning_mispronunciation_comment:
        :param tuning_nasal_score: 调音方式鼻音得分
        :param tuning_nasal_comment:
        :param rhythm_speaking_rate_score: 韵律语速得分
        :param rhythm_speaking_rate_comment:
        :param rhythm_speech_burst_score: 韵律言语爆发得分
        :param rhythm_speech_burst_comment:
        :param rhythm_other_score: 韵律其他得分
        :param rhythm_other_comment:
        :param other_incoherence_score: 不连贯得分
        :param other_incoherence_comment:
        :param other_language_barrier_score: 言语障碍得分
        :param other_language_barrier_comment:
        :param other_feature_score: 其他特征得分
        :param other_feature_comment:
        :return:
        """
        url = f"{server_address}/call?id=experts.AddHearingAnalysis&v="
        data = {
            "sessionId": self.session_id,
            "materialFileId": material_file_id,
            "SampleFileId": sample_file_id,
            "criminalCaseId": case_id,
            "recodeState": recode_state,
            "analysisRecode": [
                {
                    "tab": "音高",
                    "content": [
                        {
                            "title": "音高水平",
                            "score": pitch_level_score,
                            "comment": pitch_level_comment
                        },
                        {
                            "title": "变异范围(音高)",
                            "score": pitch_variation_range_score,
                            "comment": pitch_variation_range_comment
                        },
                        {
                            "title": "音高模式",
                            "score": pitch_model_score,
                            "comment": pitch_model_comment
                        }
                    ]
                },
                {
                    "tab": "嗓音特质",
                    "content": [
                        {
                            "title": "总体",
                            "score": throat_allover_score,
                            "comment": throat_allover_comment
                        },
                        {
                            "title": "气泡音",
                            "score": throat_bubble_score,
                            "comment": throat_bubble_comment
                        },
                        {
                            "title": "其他(嗓音特质)",
                            "score": throat_other_score,
                            "comment": throat_other_comment
                        }
                    ]
                },
                {
                    "tab": "音强",
                    "content": [
                        {
                            "title": "变异范围(音强)",
                            "score": tone_intensity_score,
                            "comment": tone_intensity_comment
                        }
                    ]
                },
                {
                    "tab": "方言",
                    "content": [
                        {
                            "title": "地区",
                            "score": dialect_area_score,
                            "comment": dialect_area_comment
                        },
                        {
                            "title": "外语",
                            "score": dialect_foreign_language_score,
                            "comment": dialect_foreign_language_comment
                        },
                        {
                            "title": "个人习语",
                            "score": dialect_idiom_score,
                            "comment": dialect_idiom_comment
                        }
                    ]
                },
                {
                    "tab": "调音方式",
                    "content": [
                        {
                            "title": "元音",
                            "score": tuning_vowel_score,
                            "comment": tuning_vowel_comment
                        },
                        {
                            "title": "辅音",
                            "score": tuning_consonant_score,
                            "comment": tuning_consonant_comment
                        },
                        {
                            "title": "错误发音",
                            "score": tuning_mispronunciation_score,
                            "comment": tuning_mispronunciation_comment
                        },
                        {
                            "title": "鼻音",
                            "score": tuning_nasal_score,
                            "comment": tuning_nasal_comment
                        }
                    ]
                },
                {
                    "tab": "韵律特征",
                    "content": [
                        {
                            "title": "语速",
                            "score": rhythm_speaking_rate_score,
                            "comment": rhythm_speaking_rate_comment
                        },
                        {
                            "title": "言语爆发",
                            "score": rhythm_speech_burst_score,
                            "comment": rhythm_speech_burst_comment
                        },
                        {
                            "title": "其他(韵律特征)",
                            "score": rhythm_other_score,
                            "comment": rhythm_other_comment
                        }
                    ]
                },
                {
                    "tab": "其他特征",
                    "content": [
                        {
                            "title": "不连贯",
                            "score": other_incoherence_score,
                            "comment": other_incoherence_comment
                        },
                        {
                            "title": "言语障碍",
                            "score": other_language_barrier_score,
                            "comment": other_language_barrier_comment
                        },
                        {
                            "title": "其他(其他特征)",
                            "score": other_feature_score,
                            "comment": other_feature_comment
                        }
                    ]
                }
            ]
        }
        # analysisRecode的值是一个json字符串
        data['analysisRecode'] = json.dumps(data.get('analysisRecode'))
        res = get_response(url, data)
        return res

    def list_hearing_analysis(self, case_id):
        """
        获取听觉量化分析记录
        :param case_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.ListHearingAnalysis&v="
        data = {
            "criminalCaseId": case_id,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def del_hearing_analysis(self, case_id: str, material_file_id: str, sample_file_id: str):
        """
        删除听觉量化分析记录
        :param sample_file_id:
        :param case_id:
        :param material_file_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.DelHearingAnalysis&v="
        data = {
            "SampleFileId": sample_file_id,
            "criminalCaseId": case_id,
            "materialFileId": material_file_id,
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def add_case_classify(self, classify_name, parent_id=''):
        """
        新增一级案件分类
        :param classify_name: 案件分类名称
        :param parent_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.addCriminalCaseType&v="
        data = {
            "sessionId": self.session_id,
            "parentId": parent_id,
            "name": classify_name
        }
        res = get_response(url, data)
        return res

    def list_all_case_classify(self):
        """
        列出所有案件分类
        :return:
        """
        url = f"{server_address}/call?id=experts.listAllCriminalCaseType&v="
        data = {
            "sessionId": self.session_id
        }
        res = get_response(url, data)
        return res

    def add_case_classify_s(self, classify_list: list):
        """
        新增二级案件分类
        :param classify_list:
        :return:
        """
        url = f"{server_address}/call?id=experts.addCriminalCaseTypes&v="
        data = {
            "sessionId": self.session_id,
            "types": classify_list
        }
        res = get_response(url, data)
        return res

    def edit_case_classify(self, classify_id, classify_name):
        """
        编辑案件分类信息（一级分类和二级分类共用一个接口）
        :param classify_id:
        :param classify_name:
        :return:
        """
        url = f"{server_address}/call?id=experts.editCriminalCaseType&v="
        data = {
            "sessionId": self.session_id,
            "typeId": classify_id,
            "name": classify_name
        }
        res = get_response(url, data)
        return res

    def remove_case_classify(self, classify_id):
        """
        删除案件分类
        :param classify_id:
        :return:
        """
        url = f"{server_address}/call?id=experts.removeCriminalCaseType&v="
        data = {
            "sessionId": self.session_id,
            "typeId": classify_id
        }
        res = get_response(url, data)
        return res


if __name__ == '__main__':
    login('yaocheng', '123456')
