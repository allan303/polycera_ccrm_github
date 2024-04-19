#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# File    :   func.py
# Time    :   2019/01/14 00:09:54
# Author  :   Jack Li
# Contact :   allanth3@163.com


'''
通用函数、方法
'''

import numbers
from functools import lru_cache
from jackutils.list_tool import find_x
# app
from . import const


@lru_cache(maxsize=128, typed=False)
def get_standard_dn(val: numbers.Real, max_val: float = None, min_val: float = None):
    '''
    Summary: 获得GB标准中的DN（平方取最近）
    '''
    ls = const.DN_LIST
    if val in ls:
        return val
    return find_x(x=val, y_list=ls, func=lambda x: x**2, maximum=max_val, minium=min_val)


@lru_cache(maxsize=128, typed=False)
def get_standard_pn(val: numbers.Real, max_val: float = None, min_val: float = None):
    '''
    Summary: 获得标准PN（取大）
    '''
    ls = const.PN_LIST
    if val in ls:
        return val
    return find_x(x=val, y_list=ls, use_larger=True, maximum=max_val, minium=min_val)


@lru_cache(maxsize=128, typed=False)
def get_standard_kw(val: numbers.Real, max_val: float = None, min_val: float = None):
    '''
    Summary: 获得标准kw(最近)
    '''
    ls = const.KW_LIST
    if val in ls:
        return val
    return find_x(x=val, y_list=ls, maximum=max_val, minium=min_val)
