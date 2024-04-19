#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-08-11

'''
提供 基础通用 Pydantic
'''
from pydantic import BaseModel, BaseConfig
from typing import Optional, List
import datetime


class BaseDbPD(BaseModel):
    '''
    从数据库提取数据
    '''
    sid: Optional[str] = ''
    create_time_local: Optional[datetime.datetime] = None
    update_time_local: Optional[datetime.datetime] = None
    is_deleted: bool = False

    class Config(BaseConfig):
        # allow_population_by_field_name = True
        # 时间类型 json 化时候自动格式化
        # json_encoders = {
        #     datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
        #     .isoformat()
        #     .replace("+00:00", "Z"),
        # }
        orm_mode = True


class BaseDbWithOwnerPD(BaseDbPD):
    '''
    Summary: 带有用户基础信息的 Base
    '''
    owner_sid: Optional[str] = None
    owner_name: Optional[str] = None
    owner_username: Optional[str] = None
    share_list: List[str] = []


class BaseListPD(BaseModel):
    '''
    Summary: List res，包含 总数量和 page 之后的list
    '''
    count: Optional[int] = 0
    count_this_page: Optional[int] = 0

    class Config:
        orm_mode = True


class SidResponese(BaseModel):
    sid: Optional[str]


class MsgResponese(BaseModel):
    msg: Optional[str] = ''


class IntResponese(BaseModel):
    count: Optional[int] = 0
