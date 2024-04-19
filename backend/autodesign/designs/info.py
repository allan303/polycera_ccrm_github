#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author : Jack Li
# Email  : allanth3@163.com
# Date   : 2021-05-25
'''
Summary: 各种信息归类的简单class
'''
from dataclasses import dataclass
import copy


@dataclass
class Consumer():
    '''
    Summary: 非运行工况，的消耗 backwash,ceb,cip
    NOTE:可用于(单次或多次)的计算
    '''
    perm_m3_use: float = 0  # 产水水耗(只有非运行时会有)
    perm_m3_produced: float = 0  # 产水增加（只有运行时）
    raw_m3_use_operate: float = 0  # 运行时 原水消耗
    raw_m3_use_not_operate: float = 0  # 非运行时 原水消耗
    raw_m3_add: float = 0  # 原水产生量（仅反洗回流）
    drain_m3_not_operate: float = 0  # 排放，无论是raw 还是 perm 还是 conc
    drain_m3_operate: float = 0  # 运行时候浓水排放
    other_feed_not_operate: float = 0  # 其他带入的水源
    other_feed_operate: float = 0  # 其他带入的水源

    @property
    def perm_m3(self):
        '''
        Summary: 净 产水量
        '''
        return self.perm_m3_produced - self.perm_m3_use

    @property
    def drain_m3(self):
        # 排放 要分 是否运行环境
        return self.drain_m3_not_operate + self.drain_m3_operate

    @property
    def raw_m3(self):
        '''
        Summary: 需要的原水量：q11 （不考虑加药）
            - 总 原水消耗 = 净产水量 + 总排放 
            - 过程中转化为 raw 的部分，可以转化为 少排放的量（drain），在总量平衡中无需单独计算
            - backwash计算时：无论是否回流到原水箱，perm_m3_use都是存在的，但是drain不确定

            要么变成产水要么排放
        '''
        return self.raw_m3_use_operate+self.raw_m3_use_not_operate - self.raw_m3_add

    @property
    def other_feed_m3(self):
        '''
        Summary: 其他工序带入的水，比如采用RO产水冲洗等
        '''
        return self.other_feed_not_operate+self.other_feed_operate

    @property
    def balance(self):
        return self.raw_m3 - self.perm_m3-self.drain_m3

    def __mul__(self, i: float):
        '''
        Summary: 乘法
        '''
        new = copy.deepcopy(self)
        new.perm_m3_use *= i
        new.perm_m3_produced *= i
        new.raw_m3_use_operate *= i
        new.raw_m3_use_not_operate *= i
        new.raw_m3_add *= i
        new.drain_m3_not_operate *= i
        new.drain_m3_operate *= i
        new.other_feed_not_operate *= i
        new.other_feed_operate *= i
        return new

    def __truediv__(self, i: float):
        '''
        Summary: 除法
        '''
        return self * (1/i)

    def __add__(self, other):
        '''
        Summary: 加法
        '''
        if not other:
            return copy.deepcopy(self)
        new = Consumer()
        new.perm_m3_produced = self.perm_m3_produced + other.perm_m3_produced
        new.perm_m3_use = self.perm_m3_use + other.perm_m3_use
        new.raw_m3_use_operate = self.raw_m3_use_operate + other.raw_m3_use_operate
        new.raw_m3_use_not_operate = self.raw_m3_use_not_operate + \
            other.raw_m3_use_not_operate
        new.raw_m3_add = self.raw_m3_add+other.raw_m3_add
        new.drain_m3_not_operate = self.drain_m3_not_operate + other.drain_m3_not_operate
        new.drain_m3_operate = self.drain_m3_operate + other.drain_m3_operate
        new.other_feed_not_operate = self.other_feed_not_operate + \
            other.other_feed_not_operate
        new.other_feed_operate = self.other_feed_operate + other.other_feed_operate
        return new


@dataclass
class RealInfo():
    '''
    Summary: 
    平衡：
        1- 产水制作 = 产水 + 产水消耗
        2- 原水 + dosing_add + 外加原水raw_m3pd_add = 产水制作 + 浓水 + 冲洗排水(raw_m3)
        3- => 原水 + raw_m3pd_add（比如反冲洗不排出） = 原水operate + 冲洗排水(raw_m3)
    '''
    rec_operate: float = 0
    rec_net: float = 0
    rec_once: float = 0
    lmh_nominal: float = 0  # 净产水通量（净产水量和总面积计算）
    lmh_operate: float = 0
    lmh_design: float = 0
    perm_m3: float = 0
    drain_m3: float = 0
    raw_m3: float = 0
    hpd: float = 24
    serie_nums: int = 1
    group_nums: int = 1

    # 分项
    drain_m3_backwash: float = 0
    drain_m3_ceb: float = 0
    drain_m3_cip: float = 0
    drain_m3_mc: float = 0
    drain_m3_operate: float = 0

    @property
    def perm_m3ph(self):
        return self.perm_m3 / self.hpd

    @property
    def perm_m3ph_per_serie(self):
        return self.perm_m3ph / self.serie_nums

    @property
    def perm_m3ph_per_group(self):
        return self.perm_m3/self.group_nums

    @property
    def raw_m3ph(self):
        return self.raw_m3 / self.hpd

    @property
    def drain_m3ph(self):
        return self.drain_m3 / self.hpd


@dataclass
class PowerChemConsumer():
    '''
    Summary: 电耗，化学品消耗
    '''
    kwh_per_day: float = 0
    kwh_per_m3: float = 0
    cip_pump_hpd: float = 0
    feed_pump_hpd: float = 0  # 同 wash
    backwash_pump_hpd: float = 0


# @dataclass
# class OtherInfo():
#     show_warning: bool = True
#     create_time_local_str: str = ''
#     version: str = '1.0'
#     project_name: str = ''
#     oem_name: str = ''
#     module_model: str = ''
#     project_remark: str = ''
#     special_note: str = ''
#     treatment_process: str = ''
#     treatment_process_note: str = ''
