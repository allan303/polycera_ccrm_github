#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-23

'''
wash 设置
'''

from dataclasses import dataclass, field
from pydantic import BaseModel
# app
from jackutils.units import UnitTime, UnitPd, UnitPd
from autodesign.designs.info import Consumer


class OptionWash(BaseModel):
    '''
    Summary: Wash 正冲洗
    '''
    is_use: bool = False  # 这个表征是否运行时间常规进行清洗
    wash_water: str = 'other'  # perm, raw, other（其他洁净水源）
    # 单列冲洗量（如果利用原水泵且没有主动设定参数，则为原水泵配置到单组的量）
    m3ph_per_train: float = 10  # 冲洗流量： 不设置即为原水泵
    duration: UnitPd = UnitPd(val=30, unit='second')  # 常规冲洗配置
    duration_add: UnitPd = UnitPd(val=15, unit='second')  # 常规冲洗配置
    interval: UnitPd = UnitPd(val=120, unit='minutes')  # 常规冲洗配置

    @property
    def duration_s(self):
        return UnitTime(**self.duration.dict()).get('s')

    @property
    def duration_add_s(self):
        return UnitTime(**self.duration_add.dict()).get('s')

    @property
    def interval_s(self):
        return UnitTime(**self.interval.dict()).get('s')

    class Config:
        orm_mode = True


default_wash_option = OptionWash()
'''
====================================== 以下dc ==================
'''


@dataclass
class Wash():
    '''
    Summary: Wash 正冲洗
        - 必须配置冲洗流量，即使不需要常规冲洗
        - 冲洗可以选择是否
        - RO系统会遇到每次开机进行冲洗
    '''
    # 来自 option
    is_use: bool  # = False  # 这个表征是否运行时间常规进行清洗
    m3ph_per_train: float  # = 0
    duration: UnitTime  # = field(default_factory=dict)
    duration_add: UnitTime  # = field(default_factory=dict)
    interval: UnitTime  # = field(default_factory=dict)
    wash_water: str  # = 'perm'  # perm, raw, other（其他洁净水源）
    # 来自其他
    train_nums_per_group_s1: int  # = 1
    group_nums: int
    times_per_day: float = 0
    # 计算
    wash_m3ph: float = 0
    wash_m3: float = 0  # 单次的流量
    one_time: Consumer = field(default_factory=Consumer)  # 不考虑组，代表整个系统
    one_day_per_group: Consumer = field(default_factory=Consumer)  # 整个系统 每天消耗
    one_day_total: Consumer = field(default_factory=Consumer)  # 整个系统

    def __post_init__(self):
        if not self.is_use:
            return None
        self.set_unit_uc()
        self.cal()
        self.set_consumer()

    def set_unit_uc(self):
        self.duration = UnitTime(**self.duration)
        self.duration_add = UnitTime(**self.duration_add)
        self.interval = UnitTime(**self.interval)

    def cal(self):
        '''
        Summary: 计算流量等
            1) 选择 利用进水泵
                - 可以设置流量，如果流量>feed_tph，则默认 放大feed_pump,但是wash时候提高频率
                - 不设置流量，则默认 流量= feed
        '''
        # 就是feed pump (主动设置或没有设置 冲洗量)
        self.wash_m3ph = self.m3ph_per_train * self.train_nums_per_group_s1
        self.wash_m3 = self.wash_m3ph * self.duration.get('hours')  # 全部组单次tph

    def set_consumer(self):
        '''
        Summary: 统一
        '''
        #  ['raw','perm','other']
        self.one_time.drain_m3_not_operate = self.wash_m3  # 排放总是增加的
        if self.wash_water == 'raw':
            # 原水冲洗，消耗原水
            self.one_time.raw_m3_use_not_operate = self.wash_m3
        elif self.wash_water == 'perm':
            self.one_time.perm_m3_use = self.wash_m3
        else:
            self.one_time.other_feed_not_operate = self.wash_m3
        self.one_day_per_group = self.one_time * self.times_per_day
        self.one_day_total = self.one_day_per_group * self.group_nums
