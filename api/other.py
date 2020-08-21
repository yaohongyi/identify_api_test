#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import json
import random
import re
import string
import xlrd
import logging
import configparser
import requests
import time
import os


def get_ini_path():
    sep = os.path.sep
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取上一级目录
    parent_path = current_path.split(sep)[:-2]
    # 获取ini文件路径
    ini_path = sep.join(parent_path) + sep + 'config' + sep + 'config.ini'
    return ini_path


def get_report_path():
    sep = os.path.sep
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取上一级目录
    parent_path = current_path.split(sep)[:-2]
    # 获取ini文件路径
    report_path = sep.join(parent_path) + sep + 'report'
    return report_path


def create_random_str(str_len: int = 13):
    """生成随机字符串"""
    str_range = random.sample(string.ascii_letters, str_len)
    random_str = ''.join(str_range)
    return random_str


# 从excel读取数据:row_now为序号中的数字，不是excel的行号
def read_excel(case_title: str, sheet_name='鉴定系统接口自动化', excel_path='./test_case.xlsx') -> dict:
    excel = xlrd.open_workbook(excel_path)
    sheet = excel.sheet_by_name(sheet_name)
    case_title_list = sheet.col_values(0)
    index_num = case_title_list.index(case_title)
    cell_value = sheet.cell_value(index_num, 2).split('\n')
    data = {}
    for i in cell_value:
        key_value = i.split('=')
        key, value = key_value[0], key_value[1]
        data[key] = value
    return data


def log_config():
    root_logger = logging.getLogger()
    root_logger.setLevel('INFO')
    basic_format = "%(asctime)s [%(levelname)s] %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(basic_format, date_format)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    root_logger.addHandler(sh)


log_config()
config_path = get_ini_path()


def get_config(key: str, values: str):
    cf = configparser.ConfigParser()
    cf.read(config_path, encoding='utf-8-sig')
    config = cf.get(key, values)
    return config


client_version = get_config('base_info', 'client_version')


def get_response(url: str, data: dict):
    # 定义全局请求包头
    headers = {
        "Content-Type": "application/json",
        "Client-Version": client_version
    }
    # 从请求url中获取接口名
    interface_name = re.match(r'.*experts.(.*?)&v=', url).group(1)
    response = requests.post(url, data=json.dumps(data), headers=headers).json()
    request_json = json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ':'))
    logging.info('Interface {} Request data：\n {}'.format(interface_name, request_json))
    response_json = json.dumps(response, indent=4, ensure_ascii=False, separators=(',', ':'))
    logging.info('Interface {} Response data：\n {}'.format(interface_name, response_json))
    return response


case_name_prefix = get_config('base_info', 'case_name_prefix')


def create_case_name():
    """生成案件名"""
    now_time = time.time()
    case_name = case_name_prefix + str(int(now_time * 1000))
    return case_name


def get_file_name(file_path: str):
    """"""
    file_name = os.path.split(file_path)[-1]
    return file_name


def find_object_from_list(res: dict, list_name: str, target_object_value: str, source_object: str) -> bool:
    """
    从鉴定接口响应中查找对象是否存在
    :param res: 接口响应
    :param list_name: 接口响应中list的字段名
    :param target_object_value: 查找关键字
    :param source_object: 接口响应中字段
    :return: 查找结果
    """
    find_result = False
    has_error = res.get('hasError')
    if has_error is False:
        object_list = res.get('data').get(list_name)
        if object_list:
            for i in object_list:
                source_object_value = i.get(source_object)
                if target_object_value == source_object_value:
                    find_result = True
                    break
        else:
            find_result = False
    return find_result


if __name__ == '__main__':
    print()

