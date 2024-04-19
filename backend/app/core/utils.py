#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2019-11-21
'''
通用工具
'''

import os
import json
from typing import Iterable, List, Sequence
import itertools
import bisect
import copy
import numbers
import string
import random
import datetime
import warnings
from decimal import Decimal
from functools import lru_cache
import logging


def can(perm: dict,
        is_su: bool,
        user_sid: str,
        model: str,  # 必须提供
        action: str = None,
        scope: str = 'me',
        owner_sid: str = None,
        share_list: List[str] = None,
        qs: "QuerySet" = None):
    '''
    Summary: 权限判定, 一个用户 对 一个对象（或无对象），但是无法应对 QuerySet ，如 download_many等
    action : 操作名称
    NOTE: 即使是SU也不可编辑其他人创建的信息，但是可以删除
    perm结构：
        {
            "auth": {},
            "comment": {
                "read": "total",
                "edit": "me",
                "delete": "me",
                "clone": "me",
                "dashboard": "me"
            },
            "post": {
                "create": "me",
                "read": "me",
                "edit": "me",
                "delete": "me",
                "clone": "me",
                "dashboard": "me"
            }
        }
    '''

    if not user_sid:
        return False
    # if action in ['create', 'dashboard']:
    #     owner_sid = None
    # perm['post']
    model_actions_dt: dict = perm.get(model, {})
    # perm['post']['edit'] = 'me' or 'total'
    my_scope: str = model_actions_dt.get(action, 'me')
    # if not my_scope in ['me', 'total']:
    #     my_scope = 'me'
    # read加上 share_list 判定
    if action == 'read' and share_list:
        if user_sid in share_list:
            print('true 1')
            return True
        if 'all' in share_list:
            print('true 2')
            return True
    # 编辑比较特殊，只能编辑自己的
    if action == 'edit':
        if owner_sid:
            print('true or false 1')
            return user_sid == owner_sid
        else:
            print('true or false 2')
            return is_su or (action in model_actions_dt)
        print('false 1')
        return False
    # 除了编辑，su全部true
    if is_su:
        print('true 3')
        return True
    # model 不在权限列表中
    if not model_actions_dt:
        print('false 2')
        return False
    # 未提供 action 名称，只判断模块是否开启 can(model='post')
    if not action:
        print('true 4')
        return True
    if not action in model_actions_dt:
        # action 不在 权限dict中
        print('not action in model_actions_dt')
        return False
    if action in ['create']:  # 不需要scope的action
        print('ture or false 6')
        return action in model_actions_dt
    # 判断针对qs的情况
    if qs:
        print('qs')
        # 如果提供了QuerySet，则意味着针对某一个集合
        if my_scope == 'total':
            print('true 5')
            return True
        else:
            try:
                # 存在非我的ins
                if qs.filter(owner_sid__ne=user_sid).first():
                    print('false 3')
                    return False
                print('true 6')
                return True
            except Exception as e:
                raise e
                print('false 4')
                return False
    # 都有，开始判断针对具体instance的权限
    # 1 - No owner_sid,
    # 2 - 应该是无主的模块，如product 模块； 另一种情况是此obj出现了问题，没有写入owner
    if not owner_sid:
        # 如 list-total, product model等情况
        if scope == 'me':
            print('true or false 3')
            return True
        else:
            # print('can7')
            print('true or false 4')
            return my_scope == 'total'
    # 有owner_sid的instance (必须经过上述的判定，可能以前有模块权限时候创建，但是现在没有模块权限)
    if owner_sid == user_sid:
        print('true 7')
        return True
    print('true or false 5')
    return my_scope == 'total'


def create_logger(name: str, path: str):
    # create logger
    logger_name = name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # create file handler
    log_path = path
    fh = logging.FileHandler(log_path)
    # fh.setLevel(logging.INFO)
    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
