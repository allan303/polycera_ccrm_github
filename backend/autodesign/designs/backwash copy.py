#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2020-04-20

'''
Backwash class 化
NOTE ： 针对1组
'''
from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Optional
import math
# app
from jackutils.units import UnitPressure, UnitTime, UnitPd, UnitPd
from autodesign.designs.info import WaterConsumer


class OptionBackwash(BaseModel):
    '''
    Summary:  backwash
    '''
    is_use: bool = True
    group_nums_per_backwash: int = 4  # 交替服务 数量
    is_drain_out: bool = True  # 是否排出系统（TMF就不是排出系统，计算水耗需要）
    use_wash: bool = False  # 反洗时候保持正冲
    backwash_wash_m3ph_per_train: Optional[float] = None  # = 40 #采用系统冲洗量的百分比
    lmh: float = 150  # 反洗通量
    pressure: UnitPd = UnitPd(val=1.7, unit='bar')  # 增压
    duration: UnitPd = UnitPd(val=30, unit='seconds')
    # NOTE：反洗周期应该==制水周期，即 30s 反洗 + 30分钟制水 + 30s反洗+30s切换阀门，实际周期应该是 31分钟
    interval: UnitPd = UnitPd(val=30, unit='minutes')
    duration_add: UnitPd = UnitPd(val=30, unit='seconds')  # 其他耗时，如阀门切换

    class Config:
        orm_mode = True

    @property
    def duration_s(self):
        return UnitTime(**self.duration.dict()).get('s')

    @property
    def duration_add_s(self):
        return UnitTime(**self.duration_add.dict()).get('s')

    @property
    def interval_s(self):
        return UnitTime(**self.interval.dict()).get('s')+self.duration_s+self.duration_add_s


default_backwash_option = OptionBackwash()
'''
============================================= dc ===========================
'''


@dataclass
class Backwash():
    '''
    Summary: 反洗
    '''
    # 以下来自Option
    is_use: bool  # = False
    group_nums_per_backwash: int
    # 是否排出系统（TMF就不是排出系统，计算水耗需要）
    # NOTE: 如果不排出，则水量平衡时候需要增加产水量，以抵消反洗水增加的原水
    is_drain_out: bool  # = True
    use_wash: bool  # = True  # 反洗时候保持正冲，NOTE: 冲洗采用原水
    backwash_wash_m3ph_per_train: float  # 采用系统反冲洗
    lmh: float  # = 100  # 反洗通量
    pressure: UnitPressure  # = field(default_factory=UnitPressure)  # 增压
    duration: UnitTime  # = field(default_factory=UnitTime)
    # NOTE：反洗周期应该==制水周期，即 30s 反洗 + 30分钟制水 + 30s反洗，实际周期应该是 30.5分钟
    interval: UnitTime  # = field(default_factory=UnitTime)
    duration_add: UnitTime  # = field(default_factory=UnitTime)   # 其他耗时，如阀门切换
    # 以下来自 系统其他部分(按照group)
    times_per_day: float
    wash_m3ph_per_train: float  # = 0
    fa: float  # = 0  # 来自 main_balance
    train_nums_per_group_s1: int  # 多少列
    group_nums: int
    # 计算
    backwash_nums: int = 1
    backwash_m3ph: float = 0
    wash_m3ph: float = 0
    backwash_m3: float = 0
    wash_m3: float = 0
    one_time: WaterConsumer = field(
        default_factory=WaterConsumer)  # 不考虑组，代表整个系统
    one_day_per_group: WaterConsumer = field(
        default_factory=WaterConsumer)  # 整个系统 每天消耗
    one_day_total: WaterConsumer = field(default_factory=WaterConsumer)  # 整个系统

    def __post_init__(self):
        if not self.is_use:
            return None
        self.backwash_nums = math.ceil(
            self.group_nums/self.group_nums_per_backwash)
        self.set_unit_uc()
        self.set_m3ph()
        self.set_consumer()

    # @property
    # def hpd(self):
    #     '''
    #     Summary: 当日运行时间 (包含了 duration_add)
    #     '''
    #     return self.time_detail.waste_seconds_per_day / 3600

    @property
    def hpd_backwash_pump(self):
        '''
        Summary: 反洗泵一天运行时间
        '''
        return self.duration.get('hours') * self.times_per_day

    def set_unit_uc(self):
        # 将pd中的dict转为 UnitMixin类
        self.pressure = UnitPressure(**self.pressure)
        self.duration = UnitTime(**self.duration)
        self.interval = UnitTime(**self.interval)
        self.duration_add = UnitTime(**self.duration_add)

    @property
    def duration_total(self) -> UnitTime:
        '''
        Summary: 反洗总过程时间
        '''
        return self.duration+self.duration_add

    def set_m3ph(self):
        '''
        Summary: 计算水量相关信息
        '''
        # 设置 冲洗流量
        if not self.backwash_wash_m3ph_per_train:
            self.backwash_wash_m3ph_per_train = self.wash_m3ph_per_train
        if not self.backwash_wash_m3ph_per_train:
            self.use_wash = False
        # 设置反洗数据
        self.backwash_m3ph = self.lmh * self.fa / 1000  # 反洗流量
        self.backwash_m3 = self.backwash_m3ph * \
            self.duration.get('hours')  # 单次
        # 设置wash 数据 （每次一组）
        if self.use_wash:  # 如果同时采用冲洗
            self.wash_m3ph = self.backwash_wash_m3ph_per_train * self.train_nums_per_group_s1
            self.wash_m3 = self.wash_m3ph * self.duration.get('hours')

    def set_consumer(self):
        # 设置总的每天数据
        self.one_time.perm_m3_use = self.backwash_m3  # 产水减少
        if self.is_drain_out:  # 反洗正常排出系统
            self.one_time.drain_m3_not_operate = self.backwash_m3 + self.wash_m3
            self.one_time.raw_m3_use_not_operate = self.wash_m3  # 原水排出系统
            self.one_time.perm_m3_use = self.backwash_m3  # 产水排出系统
        else:  # 不排出系统 ,wash 部分还是回去，不参与计算
            self.one_time.perm_m3_use = self.backwash_m3  # 产水消耗
            self.one_time.raw_m3_add = self.backwash_m3  # 原水增加
        self.one_day_per_group = self.one_time * self.times_per_day
        self.one_day_total = self.one_day_per_group * self.group_nums

    @property
    def drain_water_summary(self):
        '''
        Summary: 反洗水去向
        '''
        if self.is_drain_out:
            return '反洗水排空'
        else:
            return '反洗水回到原水箱(不排放)'
