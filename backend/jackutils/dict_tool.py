#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-06-08

'''
Summary: Dict
'''
import copy
from typing import List


def deep_update_dict(d: dict, u: dict) -> dict:
    # 用于深度 update  dict
    d = copy.deepcopy(d)
    if not u:
        return d
    for k, v in u.items():
        if isinstance(v, dict):
            r = deep_update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def mongoengine_handle_filter_dt(filter_dt: dict, fields_dt: dict) -> dict:
    '''
    Summary: 清洗 filter_dt
    NOTE:mongoengine格式
    '''
    # 清洗无效筛选条件，不然会导致结果为[]
    if not filter_dt:
        return {}
    dt = {}
    for k in filter_dt.keys():
        if '__' in k:
            keyls = str(k).split('__')
            # 可能存在 xx__not__mod等操作方式
            k0 = keyls.pop(0)
            if k0 in fields_dt:
                if check_mongoengine_operators(*keyls):
                    dt[k] = filter_dt[k]
        else:
            if k in fields_dt:  # 有效属性
                dt[k] = filter_dt[k]
    filter_dt = dt
    return filter_dt


def dict_to_list(dt: dict, key_text: str = 'key', value_text: str = 'value') -> List:
    '''
    Summary: 将 dict 转换为 List[Dict]
    '''
    return [{key_text: k, value_text: v} for k, v in dt.items()]
