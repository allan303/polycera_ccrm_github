#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-04-10

'''
Summary: 编制 产品目录
'''
import copy
import pandas as pd
from jackutils.json_tool import get_from_json, save_to_json
from autodesign.core.config import JSON_DEST, JSON_DEST_DESIGN_OPTION

'''
Summary: 首先从json文件获取目录
'''
PRODUCT_CATALOG_DICT = get_from_json(
    filename='product_catalog.json', dirpath=JSON_DEST)


def get_product_by_key(key, dt: dict):
    '''
    Summary: 根据key 获得 children中的信息
        - 继承parent属性
        - dt结构为 {product_name:..,children:{}}
    '''
    if not key in dt['children']:
        print(f'不在目录中')
        return dt
    # NOTE:如果不加.copy()，则get_product_dt函数错误
    # 如果加了，则生成json故障
    dt1 = dt['children'].get(key)
    # dt1 = dt['children'].get(key).copy()
    # Children 中未明确指定的属性，继承parent，这样可以统一设定
    for x in dt.keys():
        if not x in dt1:
            dt1[x] = dt[x]
    if not dt1.get('catalog'):
        dt1['catalog'] = key
    else:
        dt1['catalog'] = dt1['catalog']+f'.{key}'
    return dt1


def get_product_dt(id_str: str) -> str:
    '''
    Summary: 通过类似 '1.1.2'的编号，获取 产品类目
    Children 中未明确指定的属性，继承parent，这样可以统一设定
    '''
    if not id_str:
        return ''
    ls = str(id_str).split('.')
    dt = PRODUCT_CATALOG_DICT.copy()
    while ls:
        dt = get_product_by_key(ls[0], dt=dt)
        ls.pop(0)  # 删除第一项
    if not dt:
        return '不在目录中'
    return dt


def create_flat_json(dt: dict, save_dir: str = JSON_DEST):
    '''
    Summary: 通过tree数据结构 转换为 单层结构，之后保存为json
    '''
    BLANK = {}  # 用于存储
    # print("create_flat_json")

    def flat_product_dt(dt: dict) -> dict:
        # Summary: 将tree结构的dict转化为单层结构dict，便于后续使用
        # - dt结构为 {product_name:..,children:{}}
        if dt['children']:
            for k, v in dt['children'].items():
                pd = get_product_by_key(key=k, dt=dt)
                BLANK[pd['catalog']] = pd  # 增加属性 catalog，并且作为key
                flat_product_dt(dt=v)
        return None

    def save_flat_product_catalog(dt: dict):
        dt = dt.copy()
        flat_product_dt(dt=dt)
        for k, v in BLANK.items():
            del BLANK[k]['children']
            if v.get('product_name_en'):
                v['product_name_en'] = str(v['product_name_en']).title()
        save_to_json(data=BLANK, filename='flat_product_catalog.json',
                     dirpath=save_dir)

    save_flat_product_catalog(dt=dt)
    return None


# 每次都运行一次
# create_flat_json(dt=PRODUCT_CATALOG_DICT, save_dir=JSON_DEST)
# create_flat_json(dt=SPECTABLE_UF_DEFAULT_DICT, save_dir=JSON_DEST_DESIGN_OPTION)

# 从json文件直接提取，便于使用

FLAT_PRODUCT_CATALOG = get_from_json(
    dirpath=JSON_DEST, filename='flat_product_catalog.json')


def get_flat_product_catalog_df(dt: dict = FLAT_PRODUCT_CATALOG) -> pd.DataFrame:
    '''
    Summary: 获得DF
    '''
    fillna_values = {'class_name': '',
                     'catalog': '0',
                     'product_name': '',
                     'product_name_en': '',
                     'brand': '',
                     'model': '',
                     'cad_tag': '',
                     'standard': 'cn',
                     'description': '',
                     'unit': '',
                     'spec': '',
                     'weight_net': 0,
                     'weight_pack': 0,
                     'module_size': '',
                     'size_pack': '',
                     'material': 'PVC',
                     'dn_related': False,
                     'kw_related': False,
                     'pn_related': False,
                     'power': '',
                     'kw': 0,
                     'kw_k': 0,
                     'name': '',
                     'pid_id': '',
                     'label': '',
                     'place': '',
                     'sort_id': 0,
                     'required': True,
                     'warning': '',
                     'remark': '',
                     'nums': 0,
                     'nums_backup': 0,
                     'hpd': 0,
                     'q': 0,
                     'q_min': 0,
                     'q_max': 0,
                     'p': 0,
                     'p_min': 0,
                     'p_max': 0,
                     's': 0,
                     'pn': 0,
                     'pn_min': 0,
                     'pn_max': 0,
                     'dn': 0,
                     'dn_inch': '',
                     'dn_max': 0,
                     'dn_min': 0,
                     'pipe': None,
                     'length_m': 0,
                     'real_s': 0}
    df = pd.DataFrame(dt.values())
    df.fillna(value=fillna_values, inplace=True)
    return df
