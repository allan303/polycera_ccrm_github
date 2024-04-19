#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-11-03
'''
Summary: Models Utils
'''
from typing import List, Dict
import datetime
from .user.models import BaseDocumentOwner
from .all import MODELS_DT


def get_father(ins: BaseDocumentOwner, name: str):
    '''
    Summary: 获取father类
    return: 单个 ins 或者 None
    example: post1.get_father('project') -> ProjectOrm.get_by_sid(sid=post1.project_sid)
    '''
    if not ins:
        raise ValueError('ins为NONE')
    orm_class = MODELS_DT.get(name, None)
    if not orm_class:
        raise ValueError(f'{name} 不在 MODELS_DT 中')
    fathers = str(ins._father).split(',')
    if not name or not name in fathers:
        raise ValueError(
            f'{name} 不在 Class [{ins.__class__._classname}] _father 中')
    father_sid = getattr(ins, f'{name}_sid')
    return orm_class.get_by_sid(sid=father_sid)


def get_children(ins: BaseDocumentOwner, name: str, order_by: str = None):
    '''
    Summary: 获取children类
    return: QuerySet
    example: project1.get_child('post') -> PostOrm.objects(project_sid=project.sid).all()
    '''
    if not ins:
        raise ValueError('ins为NONE')
    orm_class = MODELS_DT.get(name, None)
    if not orm_class:
        raise ValueError(f'{name} 不在 MODELS_DT 中')
    children = str(ins._children).split(',')
    if not name or not name in children:
        raise ValueError(
            f'{name} 不在 Class [{ins.__class__._classname}] _children 中')
    return orm_class.get_qs(filter_dt_and={f'{ins._classname}_sid': ins.sid}, order_by=order_by)


def merge_to(ins: BaseDocumentOwner, sid: str):
    '''
    Summary: 将某个ins 合并到另一个里面，主要是附属的信息（children）都归到另一个ins旗下
    '''
    orm_class = ins.__class__
    new_ins = orm_class.get_by_sid_or_404(sid=sid)
    if ins.sid == new_ins:
        return None
    # 所有child 的 附属信息，如project_sid，都更换为新的
    print(orm_class._children)
    for child_name in orm_class._children.split(','):
        # 获取对应child_name的QuerySet, 如post，contact等
        children = get_children(ins=ins, name=child_name)
        for child in children:
            # 设置为新的sid
            att = f'{orm_class._classname}_sid'
            setattr(child, att, sid)
            child.save()
    # 原ins删除
    ins.delete()
