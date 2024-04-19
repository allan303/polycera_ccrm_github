#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-02-28


from dataclasses import dataclass
from typing import Union
from autodesign.core.mongo_utils import get_db_collection


@dataclass
class BaseDcDbMixin():
    '''
    Summary: 
    用于将 dataclass 与 数据库相关联
    '''
    collection_name: str = ''  # 产品数据库

    @property
    def collection(self):
        '''
        Summary: 本地产品数据库：collection，即 table
        '''
        if not self.collection_name:
            return None
        return get_db_collection(collection_name=self.collection_name)

    def update_from_obj(self, obj: object):
        '''
        Summary: 通过obj的attr进行设置
        '''
        keys = list(self.__dataclass_fields__.keys())
        for k in keys:
            if hasattr(obj, k):
                v = getattr(obj, k)
                if v:
                    setattr(self, k, v)

    def update_from_dt(self, dt: dict):
        '''
        Summary: 通过 一个 外部dict进行配置，要考虑数据清洗
        '''
        for k, v in dt.items():
            if hasattr(self, k):
                if v:  # v有值才设置
                    setattr(self, k, v)

    def update(self, dt: Union[dict, object]):
        '''
        Summary: 通过 dt 或 obj 进行更新
        '''
        if isinstance(dt, dict):
            self.update_from_dt(dt=dt)
        elif isinstance(dt, object):
            self.update_from_obj(obj=dt)

    @classmethod
    def init_from(cls, dt: Union[dict, object]):
        '''
        Summary: 由 dt 创建
        '''
        ins = cls()
        ins.update(dt=dt)
        return ins

    def update_from_db(self):
        '''
        Summary: 通过 数据库进行设置, init时候运行，因此可以 插入 函数
        '''
        ...
